"""File Organizer Tool - command line menu.
Run with:  python main.py          (menu)
           python main.py --gui    (window version)
"""
import os
import sys
import organizer
import duplicates
import renamer
import undo
import logger
from config import TOOL_NAME, CREATED_BY, DUPLICATE_FOLDER


def banner():
    print("\n" + "=" * 56)
    print(f"  {TOOL_NAME.upper()}")
    print(f"  File Organizer Tool  |  by {CREATED_BY}")
    print("=" * 56)


def choose_folder(current=None):
    while True:
        path = input("  Enter folder path: ").strip().strip('"').strip("'")
        path = os.path.abspath(os.path.expanduser(path)) if path else current
        if path and os.path.isdir(path):
            return path
        print("  Folder not found, try again.")


def show_plan(plan, base, limit=15):
    for src, dst in plan[:limit]:
        print(f"   {os.path.relpath(src, base)}  ->  {os.path.relpath(dst, base)}")
    if len(plan) > limit:
        print(f"   ... and {len(plan) - limit} more")


def confirm_and_apply(plan, base, action):
    if not plan:
        print("  Nothing to do.")
        return
    print(f"\n  Preview ({len(plan)} file(s)):")
    show_plan(plan, base)
    if input("\n  Apply these changes? (y/n): ").lower() != "y":
        print("  Cancelled. No files were changed.")
        return
    count, errors = organizer.apply_plan(plan, action)
    print(f"  Done. {count} file(s) processed. (You can undo this from the menu.)")
    for e in errors:
        print("  Error:", e)


def organize(folder):
    confirm_and_apply(organizer.plan_organize(folder), folder, "organize")


def find_duplicates(folder):
    print("  Scanning (this may take a moment)...")
    groups = duplicates.find_duplicates(folder)
    if not groups:
        print("  No duplicate files found.")
        return
    for i, group in enumerate(groups, 1):
        print(f"\n  Group {i}:  (original kept: {os.path.relpath(group[0], folder)})")
        for extra in group[1:]:
            print(f"     duplicate: {os.path.relpath(extra, folder)}")
    print(f"\n  {sum(len(g) - 1 for g in groups)} duplicate file(s), "
          f"about {duplicates.wasted_space(groups) / 1024:.1f} KB wasted.")
    if input(f"  Move duplicates into '{DUPLICATE_FOLDER}' folder? (y/n): ").lower() == "y":
        count, errors = organizer.apply_plan(duplicates.plan_move_duplicates(groups, folder), "duplicates")
        print(f"  Moved {count} file(s). Nothing was deleted.")
        for e in errors:
            print("  Error:", e)


def rename(folder):
    print("  Tokens: {name} old name, {n} counter (e.g. {n:03d}), {date} today")
    pattern = input("  Pattern (example: holiday_{n:03d}): ").strip()
    if not pattern:
        return
    try:
        start = int(input("  Start number [1]: ") or 1)
    except ValueError:
        start = 1
    ext = input("  Only this extension (e.g. jpg) [all files]: ").strip() or None
    plan, error = renamer.plan_rename(folder, pattern, start, ext)
    if error:
        print("  " + error)
        return
    confirm_and_apply(plan, folder, "rename")


def undo_last():
    last = undo.last_action()
    if not last:
        print("  Nothing to undo.")
        return
    print(f"  Last operation: {last['action']} ({len(last['moves'])} file(s)) at {last['time']}")
    if input("  Undo it? (y/n): ").lower() == "y":
        print("  " + undo.undo_last()[1])


def view_log():
    lines = logger.read_recent(20)
    print("\n".join("  " + l for l in lines) if lines else "  Log is empty.")


def main():
    if "--gui" in sys.argv:
        import gui
        gui.run()
        return
    banner()
    folder = choose_folder()
    while True:
        print(f"\n  Working folder: {folder}")
        print("   1. Organize files by category")
        print("   2. Find duplicate files")
        print("   3. Batch rename files")
        print("   4. Undo last operation")
        print("   5. View operation log")
        print("   6. Change folder")
        print("   7. Open GUI version")
        print("   0. Exit")
        c = input("\n  Your choice: ").strip()
        print()
        if c == "1":
            organize(folder)
        elif c == "2":
            find_duplicates(folder)
        elif c == "3":
            rename(folder)
        elif c == "4":
            undo_last()
        elif c == "5":
            view_log()
        elif c == "6":
            folder = choose_folder(folder)
        elif c == "7":
            import gui
            gui.run(folder)
        elif c == "0":
            print(f"  Thanks for using {TOOL_NAME}. Goodbye!")
            break
        else:
            print("  Invalid choice.")


if __name__ == "__main__":
    main()
