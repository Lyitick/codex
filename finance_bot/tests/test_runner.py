"""Convenience test runner."""
from pathlib import Path
import subprocess
import sys


def run() -> int:
    root = Path(__file__).resolve().parent
    return subprocess.call([sys.executable, "-m", "pytest", str(root.parent)])


if __name__ == "__main__":
    raise SystemExit(run())
