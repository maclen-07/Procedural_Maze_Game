import json
import os
from typing import List, Dict


HIGHSCORE_FILE = os.path.join(os.path.dirname(__file__), "..", "highscores.json")


def _path():
    return os.path.normpath(HIGHSCORE_FILE)


def load_scores() -> List[Dict]:
    p = _path()
    if os.path.exists(p):
        with open(p, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def save_scores(scores: List[Dict]) -> None:
    p = _path()
    with open(p, "w", encoding="utf-8") as f:
        json.dump(scores, f, indent=2)


def add_score(name: str, moves: int, level: str) -> None:
    scores = load_scores()
    scores.append({"name": name, "moves": moves, "level": level})
    save_scores(scores)


def sorted_scores() -> List[Dict]:
    scores = load_scores()
    return sorted(scores, key=lambda s: s.get("moves", 999999))
