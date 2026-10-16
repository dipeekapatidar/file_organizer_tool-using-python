"""Batch renaming with patterns.

Pattern tokens:  {name} = old name   {n} = counter   {date} = today's date
Examples:        holiday_{n:03d}   ->  holiday_001.jpg, holiday_002.jpg
                 {date}_{name}     ->  2026-10-12_photo.jpg
The file extension is always kept.
"""
import os
import re
from datetime import date
from organizer import list_files, unique_path


def plan_rename(folder, pattern, start=1, extension=None):
    """Preview: returns ([(old, new)], error_message)."""
    files = list_files(folder)
    if extension:
        ext = extension.lower() if extension.startswith(".") else "." + extension.lower()
        files = [f for f in files if os.path.splitext(f)[1].lower() == ext]
    plan, used, n = [], set(), start
    today = date.today().isoformat()
    for src in files:
        stem, ext = os.path.splitext(os.path.basename(src))
        try:
            new_stem = pattern.format(name=stem, n=n, date=today)
        except (KeyError, ValueError, IndexError):
            return [], "Invalid pattern. Use {name}, {n} or {n:03d}, and {date}."
        new_stem = re.sub(r'[<>:"/\\|?*]', "_", new_stem).strip()
        if not new_stem:
            return [], "Pattern produces an empty name."
        dst = unique_path(os.path.join(folder, new_stem + ext), used)
        used.add(dst)
        if dst != src:
            plan.append((src, dst))
        n += 1
    return plan, ""
