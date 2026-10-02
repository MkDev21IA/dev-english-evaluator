import os
import subprocess
import sys

# Add project root to sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

from main import get_git_diff

def test_git_diff():
    print("=" * 50)
    print("STAGE 1 TEST: Git Diff Detection")
    print("=" * 50)

    # 1. Check current branch
    branch_proc = subprocess.run(["git", "branch", "--show-current"], capture_output=True, text=True)
    current_branch = branch_proc.stdout.strip()
    print(f"📌 Current branch: {current_branch}")

    # 2. Run get_git_diff from main.py
    diff = get_git_diff()

    if diff:
        print("\n✅ SUCCESS: Git diff detected!")
        print("-" * 50)
        # Show first 10 lines of diff
        lines = diff.splitlines()
        preview = "\n".join(lines[:10])
        print(preview)
        if len(lines) > 10:
            print(f"... ({len(lines) - 10} more lines)")
        print("-" * 50)
    else:
        print("\nℹ️ No diff found with `git diff main..HEAD`.")
        if current_branch == "main":
            print("👉 You are currently on the 'main' branch, so `main..HEAD` has no diff.")
            print("👉 To test with a diff, create a branch with a commit:")
            print("   git checkout -b test-branch")
            print("   echo 'test' >> test.txt && git add test.txt && git commit -m 'test'")
            print("   python tests/test_01_git_diff.py")
        else:
            print(f"👉 You are on '{current_branch}', but there are no commits ahead of 'main' yet.")
            print("👉 Commit some changes to test this stage.")

if __name__ == "__main__":
    test_git_diff()
