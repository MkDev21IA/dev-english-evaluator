# Dev English Evaluator
A CLI tool that listens to your reasoning in English about `git diff main..HEAD`, evaluates it and corrects you

Recently, I was trying to increase my expertise in listening and speaking in English, because I am looking for remote jobs worldwide, everyday I read some text in English, everyday I watch videos in English, but I thought this is not sufficient, especially in Tech Area. So, I thought to develop this CLI tool to train and increase my capacity to speak in tech vocabulary and could talk with other tech guys.

I used Gemini Pro to give me some ideas and I agree to use:
- `sounddevice` to capture my audio;
- `OpenAI whisper-1` model to transcribe voice-to-text; 
- `gpt-4o-mini` to review it, evaluate it and to correct me;
- `edge-tts` to generate audio in native pronunciation;

By the way, I am using `Linux Fedora 44`, feel free to adapt to your OS and your preferred frameworks and languages.

I am also using OpenRouter but you can use OpenAI normally, just change the model names. 

## How to run the tool
1. Create a Virtual Environment with `python3 -m venv venv`
2. Activate it with `source venv/bin/activate`
3. Install the dependencies with `pip install -r requirements.txt`
4. Copy the example with `cp .env.example .env` 
5. Add your keys in `.env`
6. Run with `python main.py`

## Running from Any Repository (Global Alias)
To use this evaluator across any git repository on your machine without navigating back to this directory:

1. Add an alias to your `~/.bashrc`:
```bash
echo 'alias dev-english="'"$(pwd)"'/venv/bin/python '"$(pwd)"'/main.py"' >> ~/.bashrc
source ~/.bashrc
```

2. Go to any repository on your machine and run:
```bash
cd ~/.../other-project
dev-english
```

### Audio Storage
Temporary audio files (`speech.wav` and `feedback.mp3`) and `.env` are always saved inside the tool's directory (`dev-english-evaluator`), ensuring your other repositories stay clean and untracked.

## Testing Each Stage
You can test each component of the pipeline independently using the scripts inside the `tests/` directory:

1. **Git Diff Detection:**
   ```bash
   python tests/test_01_git_diff.py
   ```
2. **Microphone Recording:**
   ```bash
   python tests/test_02_recording.py
   ```
3. **Audio Playback (Speaker Check):**
   ```bash
   python tests/test_03_playback.py
   ```
4. **Edge-TTS Voice Synthesis:**
   ```bash
   python tests/test_04_tts.py
   ```
5. **Speech-to-Text (Whisper via OpenRouter):**
   ```bash
   python tests/test_05_whisper.py
   ```
6. **LLM Evaluation (GPT-4o-mini via OpenRouter):**
   ```bash
   python tests/test_06_llm_eval.py
   ```

## Attention
`git diff main..HEAD` assumes you will always create a new branch, make changes and open a PULL REQUEST to the main.

You can change that to `git diff @{u}..HEAD` or `git diff HEAD` if you prefer.
