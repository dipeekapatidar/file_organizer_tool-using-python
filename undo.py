"""Keeps a history of move/rename operations so the last one can be undone."""
import json
import os
import shutil
from datetime import datetime
from config import HISTORY_FILE, LOG_DIR, MAX_UNDO_HISTORY
from logger import log


def _load():
    if not os.path.exists(HISTORY_FILE):
        return []
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []


def _save(history):
    os.makedirs(LOG_DIR, exist_ok=True)
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history[-MAX_UNDO_HISTORY:], f, indent=2, ensure_ascii=False)


def record(action, moves):
    """moves = list of (old_path, new_path) that were really performed."""
    if not moves:
        return
    history = _load()
    history.append({"time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "action": action, "moves": [list(m) for m in moves]})
    _save(history)


def last_action():
    history = _load()
    return history[-1] if history else None


def undo_last():
    """Reverse the most recent operation. Returns (success, message)."""
    history = _load()
    if not history:
        return False, "Nothing to undo."
    entry = history.pop()
    restored, skipped = 0, 0
    for old, new in reversed(entry["moves"]):
        if os.path.exists(new) and not os.path.exists(old):
            os.makedirs(os.path.dirname(old), exist_ok=True)
            shutil.move(new, old)
            restored += 1
            log(f"UNDO | {new} -> {old}")
            try:                                   # remove folder if it became empty
                os.rmdir(os.path.dirname(new))
            except OSError:
                pass
        else:
            skipped += 1
            log(f"UNDO SKIPPED | {new} (missing, or original name already in use)")
    _save(history)
    msg = f"Undid '{entry['action']}' from {entry['time']}: {restored} file(s) restored"
    if skipped:
        msg += f", {skipped} skipped"
    return True, msg
