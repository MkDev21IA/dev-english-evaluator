import subprocess
import sounddevice as sd
from scipy.io.wavfile import write
import numpy as np
from openai import OpenAI
from dotenv import load_dotenv
import edge_tts
import asyncio
import os
import platform
import queue

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

load_dotenv(os.path.join(BASE_DIR, ".env"))

client = OpenAI(
    base_url = os.getenv("BASE_URL"),
    api_key=os.getenv("API_KEY")
)

def get_git_diff() -> str:
    """Runs `git diff HEAD` and retrieves the commits what we added, commited, but still didn't push to the remote repository."""
    result = subprocess.run(["git", "diff", "main..HEAD"], capture_output=True, text=True)
    return result.stdout.strip()

def record_audio(filename="speech.wav", sample_rate=16000):
    """Captures microphone input using sounddevice until the user presses Enter."""
    filepath = os.path.join(BASE_DIR, filename)
    print("Press Enter to start recording your PR defense...")
    input()
    print("Recording... Press Enter again to stop.")

    q = queue.Queue()

    def callback(indata, frames, time, status):
        if status:
            print(status, flush=True)
        q.put(indata.copy())

    with sd.InputStream(samplerate=sample_rate, channels=1, dtype='int16', callback=callback):
        input()

    audio_chunks =[]
    while not q.empty():
        audio_chunks.append(q.get())

    if audio_chunks:
        recording = np.concatenate(audio_chunks, axis=0)
        write(filepath, sample_rate, recording)
        file_size_kb = os.path.getsize(filepath) / 1024
        print(f"Audio captured ({file_size_kb:.1f} KB.)")
    else:
        print("No audio data captured.")

    return filepath

def transcribe_audio(audio_path: str) -> str:
    """Sends the audio to OpenAI Whisper API or local Whisper."""
    with open(audio_path, "rb") as audio_file:
        transcript = client.audio.transcriptions.create(
            model="openai/whisper-1", # Or just "whisper-1"
            file=audio_file,
            language="en"
        )
    return transcript.text

def evaluate_defense(diff: str, transcript: str) -> dict:
    """Sends the diff and transcript to an LLM for the review and refactor."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    prompt_path = os.path.join(base_dir, "system_prompt.txt")

    with open(prompt_path, "r", encoding="utf-8") as f:
        system_instructions = f.read()

    user_data = f"""
    Git Diff:
    {diff}

    My spoken defense:
    {transcript}
    """

    response = client.chat.completions.create(
        model="openai/gpt-4o-mini", #Or just "gpt-4o-mini"
        messages=[
            {"role": "system", "content": system_instructions},
            {"role": "user", "content": user_data}
        ]
    )
    raw_content = response.choices[0].message.content

    feedback = ""
    refactor = ""
    if "REFACTOR:" in raw_content:
        parts = raw_content.split("REFACTOR:")
        feedback = parts[0].replace("FEEDBACK:", "").strip()
        refactor = parts[1].strip()
    else:
        feedback = raw_content.strip()
        refactor = transcript

    return {"feedback": feedback, "refactor": refactor}

def play_audio_file(audio_path: str):
    """Plays audio according to the operating system."""
    system = platform.system()
    if system == "Linux":
        subprocess.run(["pw-play", audio_path])
    elif system == "Darwin":  # macOS
        subprocess.run(["afplay", audio_path])
    elif system == "Windows":
        os.system(f'start {audio_path}')

async def generate_and_play_audio(text: str, audio_path: str):
    """Uses edge-tts to generate and play the native pronunciation."""
    communicate = edge_tts.Communicate(text, "en-US-ChristopherNeural")
    await communicate.save(audio_path)
    play_audio_file(audio_path)

def cleanup(*files):
    """Deletes temporary audio files."""
    for path in files:
        if path and os.path.exists(path):
            try:
                os.remove(path)
            except OSError:
                pass

def main():
    diff = get_git_diff()
    if not diff:
        print("No git diff found. Make sure you have commits on your branch compared to main.")
        return

    audio_file = None
    feedback_file = os.path.join(BASE_DIR, "feedback.mp3")

    try:
        audio_file = record_audio()
        print("Transcribing...")
        transcript = transcribe_audio(audio_file)
        print(f"\nYou said: {transcript}\n")

        print("Evaluating against git diff...")
        evaluation = evaluate_defense(diff, transcript)

        print("\n🎧 Playing native pronunciation (Listen carefully!)...")
        asyncio.run(generate_and_play_audio(evaluation['refactor'], feedback_file))

        revealed = False
        while True:
            options = "[r] Replay audio"
            if not revealed:
                options += " | [t] Reveal written feedback & refactor"
            options += " | [Enter] Exit & clean up: "

            choice = input(f"\n{options}").strip().lower()

            if choice == "r":
                print("Replaying audio...")
                play_audio_file(feedback_file)
            elif choice == "t" and not revealed:
                print(f"\n Feedback:\n{evaluation['feedback']}")
                print(f"\n Native Refactor:\n{evaluation['refactor']}")
                revealed = True
            else:
                if not revealed:
                    print(f"\n Feedback:\n{evaluation['feedback']}")
                    print(f"\n Native Refactor:\n{evaluation['refactor']}")
                break
    finally:
        cleanup(audio_file, feedback_file)
        print("\n Cleaned up temporary audio files.")

if __name__ == "__main__":
    main()
