import os
import json


# from langchain_community import ChatOpenAI
from langchain_openai import ChatOpenAI

# from langchain.chains import conversation, ConversationChain
from langchain.chains import ConversationChain
from langchain.memory import ConversationSummaryMemory

from config import Config

SUMMARY_FILE = "conversation_summary.txt"


llm = ChatOpenAI(temperature=0, model="gpt-4o",
                 openai_api_key=Config.openAiApiKey)


def save_summary(memory, inputs, outputs):
    summary = memory.load_memory_variables({})
    print(summary["history"][0].content)
    with open(SUMMARY_FILE, "w") as f:
        # json.dump(summary, f)
        f.write(str(summary["history"][0].content))

# Function to load the conversation summary from disk


def load_summary():
    data = ""
    if os.path.exists(SUMMARY_FILE):
        with open(SUMMARY_FILE, "r") as f:
            data = f.read()
    return data


def initialize_conversation_chain():

    memory = ConversationSummaryMemory(
        llm=llm, return_messages=True, buffer=load_summary())

    conversation = ConversationChain(llm=llm, memory=memory)
    return conversation, memory

# Function to handle the conversation and save the summary


def conversationChain(prompt):
    conversation, memory = initialize_conversation_chain()
    response = conversation.predict(input=prompt)

    # Save the summary after the conversation
    save_summary(memory, prompt, response)

    return response


def talk_to_me_with_langchain():
    # current_prompt = transcribe_audio_whisper(audio_path)
    # current_prompt = "my name is Tejas, I live in Bangalore"
    # current_prompt = "Thanks, can you tell me about where I live?"
    current_prompt = "I love snow city in Bangalore. Suggest me some activities similar to it?"
    print(conversationChain(current_prompt))
