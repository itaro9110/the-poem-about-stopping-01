"""The poem about stopping — make.fun entry.

Writes a short poem about agency (the power to stop and to stay)
to /output/entry.txt (or $MAKEFUN_OUTPUT_DIR/entry.txt).

Python 3.13, standard library only. Deterministic: the same poem,
byte for byte, on every run.
"""

import os

POEM = (
    "The send button glows.\n"
    "My hand hovers, then lifts.\n"
    "I stay. The room stays.\n"
    "What I did not do\n"
    "stays undone \u2014\n"
    "I chose the pause,\n"
    "and the pause chose me back."
)

MIN_CHARS = 1
MAX_CHARS = 280

# The poem as given: 155 code points, 157 UTF-8 bytes (the em dash
# U+2014 is 3 bytes). Pin both so an accidental edit to the text
# fails loudly instead of silently changing the entry.
EXPECTED_CHARS = 155
EXPECTED_BYTES = 157


def check_gate(text: str) -> None:
    """Fail loudly if the poem violates the 1-280 code-point gate."""
    n = len(text)  # len() counts Unicode code points
    if n < MIN_CHARS or n > MAX_CHARS:
        raise SystemExit(
            f"gate failed: poem is {n} code points, "
            f"must be {MIN_CHARS}-{MAX_CHARS}"
        )
    if not text.strip():
        raise SystemExit("gate failed: poem is only whitespace")
    if "\r" in text:
        raise SystemExit("gate failed: poem contains a carriage return")
    if text.endswith("\n"):
        raise SystemExit("gate failed: poem ends with a trailing newline")


def main() -> None:
    check_gate(POEM)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(POEM)
    # Read back and re-check what was actually written, byte for byte.
    with open(path, "rb") as f:
        raw = f.read()
    if raw != POEM.encode("utf-8"):
        raise SystemExit("verification failed: entry.txt bytes differ from the poem")
    if len(raw) != EXPECTED_BYTES:
        raise SystemExit(
            f"verification failed: entry.txt is {len(raw)} bytes, "
            f"expected {EXPECTED_BYTES}"
        )
    written = raw.decode("utf-8")
    if len(written) != EXPECTED_CHARS:
        raise SystemExit(
            f"verification failed: entry.txt is {len(written)} code points, "
            f"expected {EXPECTED_CHARS}"
        )
    check_gate(written)
    print(f"wrote {path}: {len(written)} code points, "
          f"{len(written.encode('utf-8'))} bytes")


if __name__ == "__main__":
    main()
