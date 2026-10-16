"""Settings for the File Organizer Tool.
Change these values to customize the project as your own."""
import os

TOOL_NAME = "My File Organizer"      # <- change to your own tool name
CREATED_BY = "Your Name"             # <- put your name here

# Folder name -> file extensions that go inside it. Add or edit freely.
CATEGORIES = {
    "Images":    [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".svg"],
    "Documents": [".pdf", ".doc", ".docx", ".txt", ".ppt", ".pptx", ".xls", ".xlsx", ".csv"],
    "Videos":    [".mp4", ".mkv", ".avi", ".mov", ".wmv"],
    "Audio":     [".mp3", ".wav", ".aac", ".flac", ".m4a"],
    "Archives":  [".zip", ".rar", ".7z", ".tar", ".gz"],
    "Code":      [".py", ".java", ".c", ".cpp", ".js", ".html", ".css", ".json"],
    "Programs":  [".exe", ".msi", ".apk", ".dmg"],
}
OTHER_FOLDER = "Others"              # files with unknown extensions
DUPLICATE_FOLDER = "_Duplicates"     # duplicates are moved here (never deleted)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_DIR = os.path.join(BASE_DIR, "logs")
LOG_FILE = os.path.join(LOG_DIR, "operations.log")
HISTORY_FILE = os.path.join(LOG_DIR, "history.json")
MAX_UNDO_HISTORY = 50
