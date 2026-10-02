import os
import sys

# Add project root to sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

from main import record_audio, transcribe_audio, cleanup

def test_whisper():
    print("=" * 50)
    print("STAGE 5 TEST: Speech-to-Text (Whisper via OpenRouter)")
    print("=" * 50)

    # 1. Check API credentials
    api_key = os.getenv("API_KEY")
    base_url = os.getenv("BASE_URL")

    if not api_key or "your_openrouter" in api_key:
        print("❌ FAIL: API_KEY is not configured in your .env file!")
        print("👉 Please edit your .env file and add your real OpenRouter API key.")
        return

    print(f"🔑 Using API endpoint: {base_url or 'Default OpenAI'}")

    test_wav = None
    try:
        print("\n🎤 Say a clear phrase in English (e.g.: 'I refactored the authentication service')")
        test_wav = record_audio(filename="test_whisper.wav")

        print("\n⏳ Sending audio to Whisper for transcription...")
        transcript = transcribe_audio(test_wav)

        print("-" * 50)
        print(f"🗣️ Transcribed text:\n\"{transcript}\"")
        print("-" * 50)

        if transcript.strip():
            print("✅ SUCCESS: Whisper transcription working properly!")
        else:
            print("⚠️ WARNING: Transcription returned an empty string. Speak louder or check mic.")

    except Exception as e:
        print(f"❌ ERROR connecting to Whisper API: {e}")
        print("👉 Verify your OpenRouter credits, API key, and internet connection.")
    finally:
        cleanup(test_wav)
        print("🧹 Cleaned up temporary audio file.")

if __name__ == "__main__":
    test_whisper()
