from google.cloud import texttospeech, speech_v1p1beta1 as gcp_speech
import os
import openai
import io
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


def listen_print_loop(responses):
    """Iterates through server responses and prints them.

    The responses passed is a generator that will block until a response
    is provided by the server.

    Each response may contain multiple results, and each result may contain
    multiple alternatives; for details, see https://goo.gl/tjCPAU.  Here we
    print only the transcription for the top alternative of the top result.

    In this case, responses are provided for interim results as well. If the
    response is an interim one, print a line feed at the end of it, to allow
    the next result to overwrite it, until the response is a final one. For the
    final one, print a newline to preserve the finalized transcription.
    """
    num_chars_printed = 0
    for response in responses:
        if not response.results:
            continue

        # The `results` list is consecutive. For streaming, we only care about
        # the first result being considered, since once it's `is_final`, it
        # moves on to considering the next utterance.
        result = response.results[0]
        if not result.alternatives:
            continue

        # Display the transcription of the top alternative.
        transcript = result.alternatives[0].transcript

        # Display interim results, but with a carriage return at the end of the
        # line, so subsequent lines will overwrite them.
        #
        # If the previous result was longer than this one, we need to print
        # some extra spaces to overwrite the previous result
        overwrite_chars = " " * (num_chars_printed - len(transcript))

        if not result.is_final:
            sys.stdout.write(transcript + overwrite_chars + "\r")
            sys.stdout.flush()

            num_chars_printed = len(transcript)

        else:
            print(transcript + overwrite_chars)

            # Exit recognition if any of the transcribed phrases could be
            # one of our keywords.
            if re.search(r"\b(exit|quit)\b", transcript, re.I):
                print("Exiting..")
                break

            num_chars_printed = 0


def voice_to_text_gcp(audio_path, rate=8000):
    with io.open(audio_path, "rb") as audio_file:
        content = audio_file.read()
    audio = gcp_speech.RecognitionAudio(content=content)

    config = gcp_speech.RecognitionConfig(
        encoding=gcp_speech.RecognitionConfig.AudioEncoding.LINEAR16,
        # sample_rate_hertz=rate,
        language_code="en-IN",
        enable_speaker_diarization=True,
        # diarization_speaker_count=2,
    )

    client = gcp_speech.SpeechClient()

    response = client.recognize(config=config, audio=audio)

    for result in response.results:
        print(
            f"Channel Tag: {result.channel_tag}, Transcript: {result.alternatives[0].transcript}")
