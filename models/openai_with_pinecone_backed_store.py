
import openai
from config import Config
import os
import json

from .text_speech_interconverters import text_to_speech_gcp, transcribe_audio_whisper


from pinecone import Pinecone, ServerlessSpec


user_id = "userId123"
openai.api_key = Config.openAiApiKey
pineCone_index_name = "user-context"
pineCone = Pinecone(api_key=Config.pineConeApiKey)


def get_pineCone_index():
    index_list = pineCone.list_indexes().get('indexes', [])
    # indexExists = lambda index_name = any(index_item["name"] == index_name for index_item in index_list)

    def indexExists(index_name): return any(
        index_item["name"] == index_name for index_item in index_list
    )
    if not indexExists(pineCone_index_name):
        pineCone.create_index(pineCone_index_name,
                              dimension=512,
                              spec=ServerlessSpec(cloud="aws",
                                                  region="us-east-1"))
    index = pineCone.Index(pineCone_index_name)
    return index


def generate_embeddings(text):
    response = openai.embeddings.create(
        input=text, model="text-embedding-3-small", dimensions=512)
    return response.data[0].embedding


def store_embeddings(context_text):
    # Create an index
    index = get_pineCone_index()

    # Upsert (add or update) embeddings
    embeddings = generate_embeddings(context_text)
    index.upsert([(user_id, embeddings)])


def get_response_with_context(prompt, context_embedding):

    message = [
        {"role": "system", "content": "You are a helpful assistant that helps me with anything. \
                Use mix of english and the language that you got input in, like Indians do in day to day life. \
                Not completely local language and not completely hindi as well.\
                    Always output your response in english writing, even if the sentence is spoken in english, hinglish or mix."},
        {"role": "user", "content": f"Context Embedding: {context_embedding}\nUser prompt: {prompt}"}
    ]

    # Combine the prompt and context embedding in a way your model can use
    # This is model-specific; ensure the model can handle such inputs
    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=message,
        max_tokens=150,
    )
    return response.choices[0].message.content


def retrieve_embeddings():
    index = get_pineCone_index()

    response = index.query(top_k=10, id=user_id)
    if response and response['matches']:
        return response['matches'][0]['values']
    return ""


def get_similar_contexts(query_embedding, top_k=5):
    return index.query(embedding=query_embedding, top_k=top_k, include_metadata=True)


def talk_to_me_with_embeddings(audio_path):
    current_prompt = transcribe_audio_whisper(audio_path)
    context_embedding = retrieve_embeddings()

    response_text = get_response_with_context(
        current_prompt, context_embedding)

    store_embeddings(response_text)
    text_to_speech_gcp(response_text)
