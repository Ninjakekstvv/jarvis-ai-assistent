import json


def extract_json(text):

    text = text.strip()

    if "```json" in text:
        text = text.replace("```json", "")

    text = text.replace("```", "")

    start = text.find("{")
    end = text.rfind("}")

    if start == -1 or end == -1:
        raise ValueError("Kein JSON gefunden.")

    return json.loads(text[start:end + 1])