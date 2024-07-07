from google.cloud import texttospeech
import openai
from config import Config
from aws import AWS
import os
import json


CONTEXT_FILE = 'context.json'


openai.api_key = Config.openAiApiKey


def transcribe_audio_whisper(audio_path):
    audio_file = open(audio_path, "rb")
    response = openai.audio.transcriptions.create(
        model="whisper-1", file=audio_file)
    return response.text


def load_context():
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


def save_context(promptAndResponseArray):
    """Save context to file."""
    with open(CONTEXT_FILE, 'w') as f:
        json.dump(promptAndResponseArray, f)


def generate_response_gpt3(messages):
    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        max_tokens=150,
    )
    return response.choices[0].message.content


def text_to_speech(text):
    response = openai.audio.speech.create(
        model="tts-1-hd",
        voice="onyx",
        input=text,
    )
    response.write_to_file("output.mp3")


# # Tatti
# def text_to_speech_polly(text, output_path="polly-output.mp3"):
#     response = AWS.polly.synthesize_speech(
#         Text=text,
#         OutputFormat='mp3',
#         VoiceId='Joanna'
#     )

#     with open(output_path, 'wb') as file:
#         file.write(response['AudioStream'].read())

# # Indian Accent
def text_to_speech_gcp(prompt):
    # Instantiates a client
    client = texttospeech.TextToSpeechClient()

    # Set the text input to be synthesized
    synthesis_input = texttospeech.SynthesisInput(text=prompt)

    # Build the voice request, select the language code ("en-US")
    # ****** the NAME
    # and the ssml voice gender ("neutral")
    voice = texttospeech.VoiceSelectionParams(
        language_code='en-IN',
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )

    # Select the type of audio file you want returned
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    # Perform the text-to-speech request on the text input with the selected
    # voice parameters and audio file type
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config)

    # The response's audio_content is binary.
    with open('output.mp3', 'wb') as out:
        # Write the response to the output file.
        out.write(response.audio_content)
        print('Audio content written to file "output-gcp"')


# prompt = transcribe_audio_whisper("/Users/tejas/Desktop/second.m4a")
# response = generate_response_gpt3(prompt)
# response = "Hi तेज़स, अच्छा वेधर का मजा ले रहे हो! So, you need to transcribe a recording to test out voice modulation end-to-end, right? क्या आप recording file provide कर सकते हो? Or specific instructions कैसे चाहिए उसके बारे में, वो बता सकते हो? \
#     Let's get started with your task!"
# text_to_speech(response)
# text_to_speech_polly(response)
# text_to_speech_gcp(response)

def build_message(contexts):
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


def talk_to_me(audio_path):

    contexts = load_context()
    # previous_prompt = context.get('prompt', '')
    # previous_response = context.get('response', '')
    message = build_message(contexts)

    # Generate current prompt and response
    current_prompt = transcribe_audio_whisper(audio_path)
    message.append({
        "role": "user",
        "content": current_prompt
    })
    print(message)

    current_response = generate_response_gpt3(message)

    contexts.append({
        "prompt": current_prompt,
        "response": current_response
    })

    # Save current context
    save_context(contexts)

    text_to_speech_gcp(current_response)
