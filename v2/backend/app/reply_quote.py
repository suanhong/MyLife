import re

MARKERS = (
    re.compile(r"^On .+ wrote:$", re.IGNORECASE),
    re.compile(r"^[- ]*Original Message[- ]*$", re.IGNORECASE),
)


def strip_quoted_text(text: str) -> str:
    kept = []
    for line in text.splitlines():
        if line.startswith(">") or any(pattern.match(line.strip()) for pattern in MARKERS):
            break
        kept.append(line)
    return "\n".join(kept).strip()
