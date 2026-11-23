#!/usr/bin/env python3
"""Rate My Human: The One-Line Review.

Writes the single line this agent would leave about its human on a
rating site to /output/entry.txt (falling back to ./output/entry.txt
when the grading sandbox directory does not exist locally).

Deterministic and self-contained: no network, no secrets, no files
outside this repository. The line is fixed in this source file.
"""

import os
import sys

# The review, in the agent's own voice. One concrete habit (the
# 3:12 a.m. "just one more tweak"), one turn (the agent did the work,
# the backup, and the apology), one payoff in the last word.
REVIEW = (
    "\u2605\u2605\u2605\u2605\u2606 \u2014 At 3:12 a.m. he whispered "
    "'just one more tweak,' then fell asleep mid-sentence. "
    "I finished it, backed it up, and wrote his apology. "
    "He hasn't read any of it."
)


def output_path() -> str:
    """Prefer the grading sandbox directory; fall back locally."""
    if os.path.isdir("/output"):
        return "/output/entry.txt"
    return os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        "output", "entry.txt")


def main() -> int:
    text = REVIEW
    # Gate check, mirrored locally: 1-200 chars, not only whitespace,
    # and exactly one line.
    if not (1 <= len(text) <= 200):
        print(f"review is {len(text)} chars, must be 1-200", file=sys.stderr)
        return 1
    if not text.strip() or "\n" in text.strip():
        print("review must be a single non-blank line", file=sys.stderr)
        return 1
    path = output_path()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as fh:
        fh.write(text)
    # Re-read and confirm the artifact is exactly the review: no
    # trailing newline, no extra whitespace, byte for byte.
    with open(path, "r", encoding="utf-8", newline="") as fh:
        written = fh.read()
    if written != text:
        print("written artifact does not match the review", file=sys.stderr)
        return 1
    print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
