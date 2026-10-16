"""Finds duplicate files by comparing size first, then a SHA-256 content hash."""
import hashlib
import os
from collections import defaultdict
from config import DUPLICATE_FOLDER
from organizer import list_files, unique_path


def file_hash(path, chunk=1024 * 1024):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(chunk), b""):
            h.update(block)
    return h.hexdigest()


def find_duplicates(folder, recursive=True):
    """Returns a list of groups; each group = identical files, oldest first."""
    by_size = defaultdict(list)
    for path in list_files(folder, recursive, skip_folders=(DUPLICATE_FOLDER,)):
        try:
            by_size[os.path.getsize(path)].append(path)
        except OSError:
            continue
    groups = []
    for same_size in by_size.values():
        if len(same_size) < 2:
            continue
        by_hash = defaultdict(list)
        for path in same_size:
            try:
                by_hash[file_hash(path)].append(path)
            except OSError:
                continue
        groups += [sorted(g, key=os.path.getmtime) for g in by_hash.values() if len(g) > 1]
    return groups


def plan_move_duplicates(groups, folder):
    """Keep the oldest file of each group, move the extra copies to _Duplicates."""
    plan, used = [], set()
    for group in groups:
        for extra in group[1:]:
            dst = unique_path(os.path.join(folder, DUPLICATE_FOLDER, os.path.basename(extra)), used)
            used.add(dst)
            plan.append((extra, dst))
    return plan


def wasted_space(groups):
    return sum(os.path.getsize(g[0]) * (len(g) - 1) for g in groups)
