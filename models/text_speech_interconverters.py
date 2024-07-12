from google.cloud import texttospeech
import os
import openai

from config import Config
from aws import AWS

openai.api_key = Config.openAiApiKey


def transcribe_audio_whisper(audio_path):
    audio_file = open(audio_path, "rb")
    response = openai.audio.transcriptions.create(
        model="whisper-1", file=audio_file)
    return response.text


def text_to_speech_polly(text, output_path="polly-output.mp3"):
    response = AWS.polly.synthesize_speech(
        Text=text,
        OutputFormat='mp3',
        VoiceId='Joanna'
    )

    with open(output_path, 'wb') as file:
        file.write(response['AudioStream'].read())


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
        print('Audio content written to file "output"')
