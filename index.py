

from models.langchain_memory_model import talk_to_me_with_langchain
from models.openai_with_file_backed_store import talk_to_me
from models.openai_with_pinecone_backed_store import talk_to_me_with_embeddings
from models.langchain_analyser import context_analyser

from models.text_speech_interconverters import voice_to_text_gcp, transcribe_audio_whisper


# prompt = talk_to_me_with_embeddings("uploaded_files/fourth.m4a")


# talk_to_me_with_langchain()

# talk_to_me("uploaded_files/first.mp3")

# essential_analyser("""
#     { role: 'user', content: 'Hi, I want to transcribe this recording.' },
#     {
#         role: 'user',
#         content: 'यह मुझे सेकंट प्रॉंट है। मुझे एक प्रॉंट के लिए कुछ कहा।'
#     },
#     {
#         role: 'user',
#         content: "Ok, my name is Tejas and I live in Bangalore. Tell me about today's weather."
#     },
#     {
#         role: 'user',
#         content: 'Do you remember my name and where I live?'
#     },
#     """)


# print(voice_to_text_gcp("mono_combined.wav"))

def print_segment(output_file_path, segments):
    with open(output_file_path, 'w') as f:
        for segment in segments:
            start_time = segment['start']
            end_time = segment['end']
            text = segment['word']
            f.write(f"{start_time} - {end_time}: {text}\n")


# print(transcribe_audio_whisper("mono_combined.wav"))
# left_tr = transcribe_audio_whisper("mono_left.wav")
# right_tr = transcribe_audio_whisper("mono_right.wav")

# left_seg = left_tr.model_extra["words"]
# right_seg = right_tr.model_extra["words"]
# print(right_tr.text)

# Write the transcription and timestamps to a file
# print_segment("left_transcription.txt", left_seg)
# print_segment("right_transcription.txt", right_seg)
# print_segment("right_transcription.txt", right_tr["segments"])

print(transcribe_audio_whisper("uploaded_files/Shubham-Tejas.mp3"))
