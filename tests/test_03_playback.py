import os
import sys
import numpy as np
from scipy.io.wavfile import write

# Add project root to sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

from main import play_audio_file, cleanup

def test_playback():
    print("=" * 50)
    print("STAGE 3 TEST: Audio Playback (Speaker/Headphone Check)")
    print("=" * 50)

    test_wav = os.path.join(BASE_DIR, "test_beep.wav")

    try:
        # Generate a gentle 1-second 440Hz test tone (A4 note)
        sample_rate = 44100
        duration = 1.0
        t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
        tone = 0.2 * np.sin(2 * np.pi * 440 * t)  # 20% volume
        audio_data = (tone * 32767).astype(np.int16)

        write(test_wav, sample_rate, audio_data)
        print("🔊 Playing 1-second test tone through your speakers/headphones...")
        play_audio_file(test_wav)
        print("✅ SUCCESS: Playback command finished without errors.")
        print("👉 Did you hear the test tone? If not, check your system volume and PipeWire/PulseAudio.")

    except Exception as e:
        print(f"❌ ERROR during playback: {e}")
    finally:
        cleanup(test_wav)
        print("🧹 Cleaned up temporary test tone.")

if __name__ == "__main__":
    test_playback()
