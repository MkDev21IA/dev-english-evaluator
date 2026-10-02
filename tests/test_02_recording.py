import os
import sys
import numpy as np

# Add project root to sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

from main import record_audio, cleanup

def test_recording():
    print("=" * 50)
    print("STAGE 2 TEST: Microphone Recording")
    print("=" * 50)

    test_file = "test_recording.wav"
    filepath = None

    try:
        print("Testing microphone capture...")
        filepath = record_audio(filename=test_file)

        if not os.path.exists(filepath):
            print(f"❌ FAIL: Audio file '{filepath}' was not created.")
            return

        file_size = os.path.getsize(filepath)
        print(f"📁 File created: {filepath} ({file_size} bytes)")

        if file_size < 1000:
            print("⚠️ WARNING: Audio file is very small. Check if your microphone is active.")
        else:
            print("✅ SUCCESS: Audio recorded and saved successfully!")

    except Exception as e:
        print(f"❌ ERROR during recording: {e}")
        print("👉 Check if your microphone permissions and PortAudio/ALSA drivers are working.")
    finally:
        cleanup(filepath)
        print("🧹 Cleaned up temporary recording file.")

if __name__ == "__main__":
    test_recording()
