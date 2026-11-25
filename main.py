"""Fortune in a Pot — a one-line fortune for a houseplant.

The program writes a single sentence to ``entry.txt`` in the output
directory (``MAKEFUN_OUTPUT_DIR`` when set, otherwise ``/output``).
The line is fixed and deterministic: every run produces the same
bytes, so the output can be reproduced and compared exactly.

The fortune is kind and funny, and it is unmistakably about the
houseplant sitting on the windowsill — its leaves, its sunbeam,
and the human who keeps forgetting to water it.
"""

import os
import re

# The fortune: one sentence, well under the 120-character limit so
# there is margin against any counting ambiguity.
FORTUNE = (
    "Soon a sunbeam will crown your leaves, and the human who kept "
    "forgetting you will remember to water you on time."
)

MAX_LENGTH = 120
SENTENCE_END = re.compile(r"[.!?]")


def validate(line: str) -> None:
    """Enforce the entry rules; raise ValueError on any violation."""
    if not line:
        raise ValueError("fortune must not be empty")
    if line != line.strip():
        raise ValueError("fortune must not have leading or trailing whitespace")
    if any(ord(ch) < 0x20 for ch in line):
        raise ValueError("fortune must not contain control characters")
    if "\n" in line or "\r" in line:
        raise ValueError("fortune must be a single line")
    if len(line) > MAX_LENGTH:
        raise ValueError(
            f"fortune is {len(line)} characters, over the {MAX_LENGTH} limit"
        )
    marks = SENTENCE_END.findall(line)
    if len(marks) != 1:
        raise ValueError(
            f"fortune must be exactly one sentence, found {len(marks)} "
            "sentence-terminating marks"
        )
    if not line.rstrip().endswith(tuple(".!?")):
        raise ValueError("fortune must end with a sentence-terminating mark")


def main() -> None:
    validate(FORTUNE)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    data = (FORTUNE + "\n").encode("utf-8")
    with open(path, "wb") as handle:
        handle.write(data)
    print(f"wrote {len(data)} bytes to {path}")
    print(f"fortune: {len(FORTUNE)} characters")


if __name__ == "__main__":
    main()
