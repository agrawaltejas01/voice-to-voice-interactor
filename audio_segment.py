# Import AudioSegment from pydub
from pydub import AudioSegment

AudioSegment.converter = "/opt/homebrew/bin/ffmpeg"
AudioSegment.ffmpeg = "/opt/homebrew/bin/ffmpeg"
AudioSegment.ffprobe = "/opt/homebrew/bin/ffprobe"

# Open the stereo audio file as
# an AudioSegment instance
stereo_audio = AudioSegment.from_file(
    file="Stereo_exotel_2.mp3",
    format="mp3"

    # file="mono_combined.wav",
    # format="wav"

)

# Calling the split_to_mono method
# on the stereo audio file
mono_audios = stereo_audio.split_to_mono()

# Exporting/Saving the two mono
# audio files present at index 0(left)
# and index 1(right) of list returned
# by split_to_mono method
mono_left = mono_audios[0].export(
    "mono_left.wav",
    format="wav")
mono_right = mono_audios[1].export(
    "mono_right.wav",
    format="wav")

# # Combine both channels into a single channel
combined = mono_audios[0].overlay(mono_audios[1])
combined.export("mono_combined.wav", format="wav")
