from .text_speech_interconverters import transcribe_audio_whisper, text_to_speech_gcp
import openai
from config import Config
import os
import json


CONTEXT_FILE = 'context.json'
openai.api_key = Config.openAiApiKey


def load_context_file():
    """Load context from file."""
    emptyResponse = [{'prompt': '', 'response': ''}]
    if os.path.exists(CONTEXT_FILE):
        with open(CONTEXT_FILE, 'r') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError as e:
                print(f"Error loading context file: {e}")
                return emptyResponse
    else:
        return emptyResponse


def build_message_from_file_context(contexts):
    messages = [
        {"role": "system", "content": "You are a helpful assistant that helps me with anything. \
                Use mix of english and the language that you got input in, like Indians do in day to day life. \
                Not completely local language and not completely hindi as well.\
                    Always output your response in english writing, even if the sentence is spoken in english, hinglish or mix."},
    ]
    for context in contexts:
        if context["prompt"] and context["response"]:
            messages.append({
                "role": "user",
                "content": context["prompt"]
            })
            messages.append({
                "role": "system",
                "content": context["response"]
            })
    return messages


def generate_response_gpt3_with_file_context(messages):
    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        max_tokens=150,
    )
    return response.choices[0].message.content


def save_context_file(promptAndResponseArray):
    """Save context to file."""
    with open(CONTEXT_FILE, 'w') as f:
        json.dump(promptAndResponseArray, f)


def talk_to_me(audio_path):

    contexts = load_context_file()
    # previous_prompt = context.get('prompt', '')
    # previous_response = context.get('response', '')
    message = build_message_from_file_context(contexts)

    # Generate current prompt and response
    current_prompt = transcribe_audio_whisper(audio_path)
    message.append({
        "role": "user",
        "content": current_prompt
    })
    print(message)

    current_response = generate_response_gpt3_with_file_context(message)

    contexts.append({
        "prompt": current_prompt,
        "response": current_response
    })

    # Save current context
    save_context_file(contexts)

    text_to_speech_gcp(current_response)
