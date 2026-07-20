import json
from pathlib import Path

DATABASE = Path("programs.json")


def load_database():

    if not DATABASE.exists():
        return {}

    try:
        with open(DATABASE, "r", encoding="utf-8") as f:
            return json.load(f)

    except Exception:
        return {}