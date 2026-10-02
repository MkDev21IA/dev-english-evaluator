import os
import sys
import asyncio

# Add project root to sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

from main import generate_and_play_audio, cleanup

def test_tts():
    print("=" * 50)
    print("STAGE 4 TEST: Edge-TTS Speech Generation & Playback")
    print("=" * 50)

    test_mp3 = os.path.join(BASE_DIR, "test_speech.mp3")
    sample_text = "Hello! This is a test of Edge TTS voice synthesis for your English evaluator."

    try:
        print(f"🗣️ Generating and playing speech: \"{sample_text}\"")
        asyncio.run(generate_and_play_audio(sample_text, test_mp3))

        if os.path.exists(test_mp3) and os.path.getsize(test_mp3) > 0:
            print("✅ SUCCESS: Edge-TTS generated audio and played it successfully!")
        else:
            print("❌ FAIL: Audio file was not created or is empty.")

    except Exception as e:
        print(f"❌ ERROR during TTS generation/playback: {e}")
        print("👉 Check your internet connection (Edge-TTS requires internet).")
    finally:
        cleanup(test_mp3)
        print("🧹 Cleaned up temporary TTS audio file.")

if __name__ == "__main__":
    test_tts()
