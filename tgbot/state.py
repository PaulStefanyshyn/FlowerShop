import json
import os

STATE_FILE = "storage/last_seen.json"


def load_state() -> dict:
    if not os.path.exists(STATE_FILE):
        return {"last_id": 0}

    with open(STATE_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def save_state(state: dict) -> None:
    os.makedirs("storage", exist_ok=True)

    with open(STATE_FILE, "w", encoding="utf-8") as file:
        json.dump(state, file, ensure_ascii=False, indent=2)