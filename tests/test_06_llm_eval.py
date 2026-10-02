import os
import sys

# Add project root to sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

from main import evaluate_defense

def test_llm_evaluation():
    print("=" * 50)
    print("STAGE 6 TEST: LLM Defense Evaluation (GPT-4o-mini via OpenRouter)")
    print("=" * 50)

    # 1. Check API credentials
    api_key = os.getenv("API_KEY")
    base_url = os.getenv("BASE_URL")

    if not api_key or "your_openrouter" in api_key:
        print("❌ FAIL: API_KEY is not configured in your .env file!")
        print("👉 Please edit your .env file and add your real OpenRouter API key.")
        return

    print(f"🔑 Using API endpoint: {base_url or 'Default OpenAI'}")

    # 2. Simulated git diff
    mock_diff = """diff --git a/services/auth.py b/services/auth.py
--- a/services/auth.py
+++ b/services/auth.py
@@ -10,3 +10,6 @@
+def validate_session(token: str) -> bool:
+    \"\"\"Validates bearer token length and prefix.\"\"\"
+    return len(token) > 10 and token.startswith("Bearer ")
"""

    # 3. Simulated spoken defense (with deliberate small grammar/phrasing issues to test the critique)
    mock_transcript = "In this commit, I made a function for validate the session token. If the token have more than ten characters and start with Bearer, it return true."

    print("\n📄 Mock Git Diff:\n" + mock_diff)
    print("🗣️ Mock Spoken Defense:\n\"" + mock_transcript + "\"\n")
    print("⏳ Sending to GPT-4o-mini for review...")

    try:
        evaluation = evaluate_defense(mock_diff, mock_transcript)

        if not isinstance(evaluation, dict):
            print(f"❌ FAIL: Expected dictionary from evaluate_defense, got {type(evaluation).__name__}")
            return

        if "feedback" not in evaluation or "refactor" not in evaluation:
            print(f"❌ FAIL: Missing 'feedback' or 'refactor' keys in result: {evaluation}")
            return

        print("\n" + "=" * 50)
        print("📝 FEEDBACK RECEIVED:")
        print("=" * 50)
        print(evaluation["feedback"])

        print("\n" + "=" * 50)
        print("💡 NATIVE REFACTOR:")
        print("=" * 50)
        print(evaluation["refactor"])

        print("\n✅ SUCCESS: LLM evaluation and parsing working perfectly!")

    except Exception as e:
        print(f"\n❌ ERROR during LLM evaluation: {e}")
        print("👉 Check your OpenRouter credits, API key, or system_prompt.txt file.")

if __name__ == "__main__":
    test_llm_evaluation()
