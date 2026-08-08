"""Python wrapper for agy -p with structured output."""
import subprocess
import json
import os
from pathlib import Path

AGY = os.environ.get("AGY_BIN", r"C:\Users\uguri\bin\agy.exe")


def agy_run(
    prompt: str,
    model: str | None = None,
    workdir: str | None = None,
    timeout: int = 180,
    output_format: str = "text",
    add_dirs: list[str] | None = None,
) -> dict:
    """Run agy -p and return structured result.

    Returns: {"stdout": str, "stderr": str, "exit_code": int}
    """
    cmd = [AGY, "-p", prompt, "--dangerously-skip-permissions",
           "--print-timeout", f"{timeout}s"]
    if model:
        cmd += ["--model", model]
    if output_format != "text":
        cmd += ["--output-format", output_format]
    if add_dirs:
        for d in add_dirs:
            cmd += ["--add-dir", d]

    result = subprocess.run(
        cmd, capture_output=True, text=True,
        timeout=timeout + 30, cwd=workdir or None,
    )
    return {
        "stdout": result.stdout,
        "stderr": result.stderr,
        "exit_code": result.returncode,
    }


if __name__ == "__main__":
    import sys
    prompt = " ".join(sys.argv[1:]) or "Say hello in one sentence."
    r = agy_run(prompt)
    print(r["stdout"])
    if r["stderr"]:
        print(f"[stderr] {r['stderr']}", file=sys.stderr)
