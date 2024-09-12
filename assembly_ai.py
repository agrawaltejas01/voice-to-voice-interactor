
# Cant do Hinglish
# import assemblyai as aai

# aai.settings.api_key = "45ac126c4b7142e7ba4ca52f39798748"
# transcriber = aai.Transcriber()

# config = aai.TranscriptionConfig(
#     speaker_labels=True, punctuate=True, speakers_expected=2)
# transcript = transcriber.transcribe(
#     "Stereo_exotel_2.mp3", config=config)

# for u in transcript.utterances:
#     print(f"Speaker {u.speaker}: {u.text}")

# print(u.text)


import speechmatics
from speechmatics.models import ConnectionSettings, BatchTranscriptionConfig
from speechmatics.batch_client import BatchClient
from httpx import HTTPStatusError

API_KEY = "45vgh8sgWkSPdPxra3XtwMvA4w1prcNm"
PATH_TO_FILE = "Stereo_exotel_2.mp3"
LANGUAGE = "en"
expectedLanguages = speechmatics.models.BatchLanguageIdentificationConfig(
    expected_languages=["en", "hi"]
)
diarisation = speechmatics.models.BatchSpeakerDiarizationConfig(
    speaker_sensitivity=1
)

# Open the client using a context manager
with BatchClient(API_KEY) as client:
    try:
        job_id = client.submit_job(
            PATH_TO_FILE, BatchTranscriptionConfig(LANGUAGE, language_identification_config=expectedLanguages, speaker_diarization_config=diarisation))
        print(f'job {job_id} submitted successfully, waiting for transcript')

        # Note that in production, you should set up notifications instead of polling.
        # Notifications are described here: https://docs.speechmatics.com/features-other/notifications
        transcript = client.wait_for_completion(
            job_id, transcription_format='txt')
        # To see the full output, try setting transcription_format='json-v2'.
        print(transcript)
    except HTTPStatusError as e:
        if e.response.status_code == 401:
            print('Invalid API key - Check your API_KEY at the top of the code!')
        elif e.response.status_code == 400:
            print(e.response.json()['detail'])
        else:
            raise e
