import re


def parse_document(file_path):

    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()

    sections = {}

    pattern = r"(.*?):\n(.*?)(?=\n[A-Z][A-Za-z ]+?:|\Z)"

    matches = re.findall(pattern, text, re.S)

    for title, content in matches:
        sections[title.strip()] = content.strip()

    return sections