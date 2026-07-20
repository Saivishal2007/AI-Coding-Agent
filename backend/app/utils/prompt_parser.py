import re


def extract_filename(prompt: str) -> str | None:
    """
    Extracts filenames such as:

    config.py
    main.py
    repository_service.py
    """

    match = re.search(r"\b[\w\-]+\.py\b", prompt)

    if match:
        return match.group(0)

    return None