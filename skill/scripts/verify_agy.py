"""Verify agy CLI is installed and authenticated."""
import subprocess
import sys

AGY = r"C:\Users\uguri\bin\agy.exe"


def main():
    checks = []

    # 1. Binary exists
    try:
        r = subprocess.run([AGY, "--version"], capture_output=True, text=True, timeout=15)
        if r.returncode == 0:
            print(f"OK agy version: {r.stdout.strip()}")
            checks.append(True)
        else:
            print(f"FAIL agy --version: {r.stderr.strip()}")
            checks.append(False)
    except Exception as e:
        print(f"FAIL agy not found: {e}")
        checks.append(False)

    # 2. Authenticated
    try:
        r = subprocess.run([AGY, "models"], capture_output=True, text=True, timeout=30)
        if "gemini" in r.stdout.lower():
            print(f"OK agy authenticated, models available")
            checks.append(True)
        else:
            print(f"WARN agy models output: {r.stdout[:200]}")
            print(f"     stderr: {r.stderr[:200]}")
            checks.append(False)
    except Exception as e:
        print(f"FAIL agy models: {e}")
        checks.append(False)

    if all(checks):
        print("\nAll checks passed.")
        return 0
    print(f"\n{sum(checks)}/{len(checks)} checks passed.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
