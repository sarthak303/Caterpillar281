import moviepy.editor as mp
import speech_recognition as sr
import os
from pydub import AudioSegment

def video_to_audio(video_file, audio_file):
    """Convert video file to audio file."""
    video = mp.VideoFileClip(video_file)
    video.audio.write_audiofile(audio_file)

def split_audio(audio_file, chunk_length=30):
    """Split audio file into smaller chunks."""
    audio = AudioSegment.from_wav(audio_file)
    chunks = []
    
    for i in range(0, len(audio), chunk_length * 1000):  # chunk_length in seconds
        chunk = audio[i:i + chunk_length * 1000]
        chunk_name = f"chunk_{i // 1000}.wav"
        chunk.export(chunk_name, format="wav")
        chunks.append(chunk_name)
    
    return chunks

def audio_to_text(audio_chunk):
    """Convert an audio chunk file to text transcription."""
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_chunk) as source:
        audio = recognizer.record(source)
    try:
        text = recognizer.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        return "[Unintelligible]"
    except sr.RequestError as e:
        return f"[Error: {e}]"

def video_to_text_transcription(video_file, audio_file="audio.wav", chunk_length=30):
    """Convert video file to text transcription."""
    video_to_audio(video_file, audio_file)
    
    # Split the audio into smaller chunks
    audio_chunks = split_audio(audio_file, chunk_length)
    
    # Transcribe each chunk and accumulate the results
    full_transcription = ""
    for chunk in audio_chunks:
        transcription = audio_to_text(chunk)
        full_transcription += transcription + " "
        os.remove(chunk)  # Clean up the chunk file after processing
    
    return full_transcription

# Example usage:
video_file = "Learn English Conversation_ Weather and Small Talk 30 SECONDS (Subtitles).mp4"
audio_file = "audio.wav"
transcription = video_to_text_transcription(video_file, audio_file)
print("Transcription:", transcription)
