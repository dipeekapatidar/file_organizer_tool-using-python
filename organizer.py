"""Core file operations: categorize files and safely move them."""
import os
import shutil
from config import CATEGORIES, OTHER_FOLDER
from logger import log
import undo


def unique_path(path, used=()):
    """If a file already exists (or is planned), add _1, _2 ... to the name."""
    if not os.path.exists(path) and path not in used:
        return path
    stem, ext = os.path.splitext(path)
    i = 1
    while os.path.exists(f"{stem}_{i}{ext}") or f"{stem}_{i}{ext}" in used:
        i += 1
    return f"{stem}_{i}{ext}"


def list_files(folder, recursive=False, skip_folders=()):
    """Visible files in a folder (hidden files are ignored)."""
    found = []
    if recursive:
        for root, dirs, files in os.walk(folder):
            dirs[:] = [d for d in dirs if not d.startswith(".") and d not in skip_folders]
            found += [os.path.join(root, f) for f in files if not f.startswith(".")]
    else:
        for name in sorted(os.listdir(folder)):
            full = os.path.join(folder, name)
            if os.path.isfile(full) and not name.startswith("."):
                found.append(full)
    return sorted(found)


def category_for(filename):
    ext = os.path.splitext(filename)[1].lower()
    for category, extensions in CATEGORIES.items():
        if ext in extensions:
            return category
    return OTHER_FOLDER


def plan_organize(folder):
    """Preview: returns [(source, destination)] without touching any file."""
    plan, used = [], set()
    for src in list_files(folder):
        dst = os.path.join(folder, category_for(src), os.path.basename(src))
        dst = unique_path(dst, used)
        used.add(dst)
        plan.append((src, dst))
    return plan


def apply_plan(plan, action):
    """Perform the moves, write the log and save the undo record."""
    done, errors = [], []
    for src, dst in plan:
        try:
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.move(src, dst)
            done.append((src, dst))
            log(f"{action.upper()} | {src} -> {dst}")
        except OSError as e:
            errors.append(f"{os.path.basename(src)}: {e}")
            log(f"ERROR | {src}: {e}")
    undo.record(action, done)
    return len(done), errors
