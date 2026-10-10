from __future__ import annotations

import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path


@dataclass
class NeverTwiceResult:
    command: list[str]
    available: bool
    exit_code: int | None
    stdout: str
    stderr: str
    verdict: str | None


def invoke(args: list[str], cwd: Path | None = None) -> NeverTwiceResult:
    executable = shutil.which("nt")
    command = ["nt", *args]
    if executable is None:
        return NeverTwiceResult(command, False, None, "", "nt executable not found", None)
    completed = subprocess.run(command, cwd=cwd, capture_output=True, text=True, check=False)
    combined = f"{completed.stdout}\n{completed.stderr}".upper()
    verdict = next((value for value in ("BLOCK", "WARN", "SAFE") if value in combined), None)
    return NeverTwiceResult(
        command, True, completed.returncode, completed.stdout, completed.stderr, verdict
    )


def supported_commands() -> dict[str, bool]:
    return {
        "check": shutil.which("nt") is not None,
        "hooks install": shutil.which("nt") is not None,
        "watch": shutil.which("nt") is not None,
    }
