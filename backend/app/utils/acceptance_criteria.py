import re


import re


def extract_acceptance_criteria(text: str) -> dict:
    pattern = re.compile(
        r"^[ \t]*AC(\d+)[ \t]*[-—–:][ \t]*(.+?)[ \t]*$",
        re.MULTILINE,
    )

    section_pattern = re.compile(
        r"^[ \t]*(Business Rules|Definition of Done|"
        r"Non-Functional Requirements|Security Requirements)"
        r"[ \t]*:?[ \t]*$",
        re.MULTILINE | re.IGNORECASE,
    )

    matches = list(pattern.finditer(text))
    criteria = {}

    for index, match in enumerate(matches):
        ac_id = f"AC{match.group(1)}"
        title = match.group(2).strip()

        start = match.end()

        if index + 1 < len(matches):
            end = matches[index + 1].start()
        else:
            end = len(text)

        # Stop before the next non-AC section
        section_match = section_pattern.search(text, start, end)

        if section_match:
            end = section_match.start()

        body = text[start:end].strip()

        # Ignore AC headings without behavioral evidence
        if not body:
            continue

        criteria[ac_id] = {
            "title": title,
            "text": body,
        }

    return criteria