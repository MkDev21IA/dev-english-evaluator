import subprocess
import sounddevice as sd
from scipy.io.wavfile import write
from openai import OpenAI
from dotenv import load_dotenv
import edge_tts
import asyncio
import os

load_dotenv()

client = OpenAI(
    base_url = os.getenv("BASE_URL"),
    api_key=os.getenv("API_KEY")
)

def get_git_diff() -> str:
    """Runs `git diff HEAD` and retrieves the commits what we added, commited, but still didn't push to the remote repository."""
    result = subprocess.run(["git", "diff", "main..HEAD"], capture_output=True, text=True)
    return result.stdout.strip

def record_audio(filename="speech.wav", sample_rate=44100):
    """Captures microphone input using sounddevice until the user presses Enter."""
    print("Press Enter to start recording your PR defense...")
    input()
    print("Recording... Press Enter again to stop.")

    recording = sd.rec(int(10 * 3600 * sample_rate), samplerate=sample_rate, channels=1)
    input()
    sd.stop()

    write(filename, sample_rate, recording)
    print("Audio captured.")
    return filename

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

async def play_audio_feedback(text: str):
    """Uses edge-tts to generate and play the native pronunciation."""
    communicate = edge_tts.Communicate(text, "en-US-ChristopherNeural")
    await communicate.save("feedback.mp3")

    subprocess.run(["pw-play", "feedback.mp3"]) # Change "pw-play" to "afplay" if your are using macOS
                                                # If you are using windows just substitute `subprocess.run(["pw-play", "feedback.mp3"])` by os.system("start feedback.mp3")
def main():
    diff = get_git_diff()
    if not diff:
        print("No git diff found. Make sure you have commits on your branch compared to main.")
        return

    audio_file = record_audio()

    print("Transcribing...")
    transcript = transcribe_audio(audio_file)
    print(f"\nYou said: {transcript}\n")

    print("Evaluating against git diff...")
    evaluation = evaluate_defense(diff, transcript)
    print(f"\nFeedback: {evaluation['feedback']}")
    print(f"Native Refactor: {evaluation['refactor']}\n")

    print("Playing native pronunciation...")
    asyncio.run(play_audio_feedback(evaluation['refactor']))

if __name__ == "__main__":
    main()
