# File Organizer Tool (Python)

A simple tool to clean up messy folders. No external libraries needed, only Python 3.8+.

## Run
    python main.py            menu version (Windows)
    python3 main.py           menu version (Mac / Linux)
    python main.py --gui      window version

## Features
- Automatic categorization (Images, Documents, Videos, Audio, Archives, Code ...)
- Duplicate detection by file content (extra copies are MOVED, never deleted)
- Batch renaming with patterns, e.g. `holiday_{n:03d}` -> holiday_001.jpg
- Preview before every change, so nothing happens without your confirmation
- Operation log in logs/operations.log
- Undo last operation (works for organize, rename and duplicate moves)
- Optional GUI built with Tkinter

## Files
| File | Purpose |
|------|---------|
| main.py | Menu and entry point |
| gui.py | Optional window interface |
| organizer.py | Categorizing and safe moving of files |
| duplicates.py | Duplicate detection (size + SHA-256 hash) |
| renamer.py | Pattern-based batch renaming |
| undo.py | Undo history |
| logger.py | Operation log |
| config.py | Tool name, categories, folder names |

## Customize
Open `config.py` and change `TOOL_NAME`, `CREATED_BY`, and the `CATEGORIES` list.
Add your own category, e.g. `"Ebooks": [".epub", ".mobi"]`.

## Safe testing
Try it first on a test folder with a few copied files, not on your important data.
