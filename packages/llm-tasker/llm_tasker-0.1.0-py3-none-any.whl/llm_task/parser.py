import json
import re
from typing import Any


JSON = r"```json([\s\S]*?)```"
BRACKETS = r"`([\s\S]*?)`"
SPLIT = r"\n\n[A-Z].*: "
json_rule = re.compile(JSON)
bracket_rule = re.compile(BRACKETS)
split_rule = re.compile(SPLIT)


def parse_json(string: str) -> dict[str, Any] | None:
    candidates = [string]
    content = str(string)

    match = json_rule.search(content) or bracket_rule.search(content)

    if match:
        json_text = match.group(1).strip()
        candidates.append(json_text)

    try:
        content, _ = split_rule.split(string, maxsplit=1)
        candidates.append(content.strip())
    except ValueError:
        pass

    for candidate in candidates:
        try:
            return json.loads(candidate)
        except json.decoder.JSONDecodeError:
            continue
