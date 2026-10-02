# Pipeline Stage Tests

These scripts allow you to independently test and debug every component of the `dev-english-evaluator` tool.

Make sure your virtual environment is active before running tests:
```bash
source venv/bin/activate
```

---

### Stage 1: Git Diff Detection
Tests if git diff detection is working properly in your repository.
```bash
python tests/test_01_git_diff.py
```

---

### Stage 2: Microphone Recording
Tests your microphone input, `sounddevice`, and audio file creation.
```bash
python tests/test_02_recording.py
```

---

### Stage 3: Audio Playback (Speaker Check)
Plays a 1-second test tone through your headphones/speakers using `pw-play` (no internet required).
```bash
python tests/test_03_playback.py
```

---

### Stage 4: Edge-TTS Speech Synthesis
Tests Microsoft Edge TTS voice generation and playback (requires internet).
```bash
python tests/test_04_tts.py
```

---

### Stage 5: Speech-to-Text (Whisper via OpenRouter)
Tests recording your voice and transcribing it using `openai/whisper-1` via your OpenRouter API key.
```bash
python tests/test_05_whisper.py
```

---

### Stage 6: LLM Evaluation (GPT-4o-mini via OpenRouter)
Sends a simulated git diff and spoken defense to `openai/gpt-4o-mini` to verify that `system_prompt.txt` is loaded, evaluated, and parsed properly into feedback and refactor.
```bash
python tests/test_06_llm_eval.py
```
