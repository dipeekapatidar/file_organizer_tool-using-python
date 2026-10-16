"""Optional window (Tkinter) version. Tkinter comes with normal Python installs."""
import os
import tkinter as tk
from tkinter import filedialog, messagebox
import organizer
import duplicates
import renamer
import undo
import logger
from config import TOOL_NAME, CREATED_BY, DUPLICATE_FOLDER


class App:
    def __init__(self, root, folder=""):
        self.root = root
        root.title(f"{TOOL_NAME} - by {CREATED_BY}")
        root.geometry("760x520")

        top = tk.Frame(root)
        top.pack(fill="x", padx=10, pady=8)
        self.folder = tk.StringVar(value=folder)
        tk.Label(top, text="Folder:").pack(side="left")
        tk.Entry(top, textvariable=self.folder, width=62).pack(side="left", padx=6)
        tk.Button(top, text="Browse", command=self.browse).pack(side="left")

        row = tk.Frame(root)
        row.pack(fill="x", padx=10)
        for text, cmd in [("Organize", self.organize), ("Find Duplicates", self.duplicates),
                          ("Undo Last", self.undo), ("View Log", self.view_log)]:
            tk.Button(row, text=text, width=16, command=cmd).pack(side="left", padx=3, pady=4)

        ren = tk.Frame(root)
        ren.pack(fill="x", padx=10, pady=4)
        tk.Label(ren, text="Rename pattern:").pack(side="left")
        self.pattern = tk.StringVar(value="file_{n:03d}")
        tk.Entry(ren, textvariable=self.pattern, width=26).pack(side="left", padx=6)
        tk.Label(ren, text="Extension (optional):").pack(side="left")
        self.ext = tk.StringVar()
        tk.Entry(ren, textvariable=self.ext, width=8).pack(side="left", padx=6)
        tk.Button(ren, text="Batch Rename", command=self.rename).pack(side="left")

        self.out = tk.Text(root, wrap="none", font=("Consolas", 10))
        self.out.pack(fill="both", expand=True, padx=10, pady=8)
        self.say(f"Welcome to {TOOL_NAME}. Choose a folder and pick an action.")

    # ---------- helpers ----------
    def say(self, text):
        self.out.insert("end", text + "\n")
        self.out.see("end")

    def get_folder(self):
        path = self.folder.get().strip()
        if not os.path.isdir(path):
            messagebox.showerror("Folder", "Please choose a valid folder first.")
            return None
        return path

    def browse(self):
        path = filedialog.askdirectory()
        if path:
            self.folder.set(path)

    def run_plan(self, plan, base, action):
        if not plan:
            self.say("Nothing to do.")
            return
        self.out.delete("1.0", "end")
        self.say(f"Preview - {len(plan)} file(s):")
        for src, dst in plan[:200]:
            self.say(f"  {os.path.relpath(src, base)}  ->  {os.path.relpath(dst, base)}")
        if messagebox.askyesno("Confirm", f"Apply {action} to {len(plan)} file(s)?"):
            count, errors = organizer.apply_plan(plan, action)
            self.say(f"\nDone: {count} file(s) processed. Use 'Undo Last' to reverse.")
            for e in errors:
                self.say("Error: " + e)
        else:
            self.say("\nCancelled. No files were changed.")

    # ---------- actions ----------
    def organize(self):
        folder = self.get_folder()
        if folder:
            self.run_plan(organizer.plan_organize(folder), folder, "organize")

    def duplicates(self):
        folder = self.get_folder()
        if not folder:
            return
        groups = duplicates.find_duplicates(folder)
        self.out.delete("1.0", "end")
        if not groups:
            self.say("No duplicate files found.")
            return
        for i, g in enumerate(groups, 1):
            self.say(f"Group {i} (kept: {os.path.relpath(g[0], folder)})")
            for extra in g[1:]:
                self.say(f"    duplicate: {os.path.relpath(extra, folder)}")
        if messagebox.askyesno("Duplicates", f"Move extra copies into '{DUPLICATE_FOLDER}'?"):
            count, _ = organizer.apply_plan(duplicates.plan_move_duplicates(groups, folder), "duplicates")
            self.say(f"\nMoved {count} file(s). Nothing was deleted.")

    def rename(self):
        folder = self.get_folder()
        if not folder:
            return
        plan, error = renamer.plan_rename(folder, self.pattern.get(), 1, self.ext.get().strip() or None)
        if error:
            messagebox.showerror("Pattern", error)
        else:
            self.run_plan(plan, folder, "rename")

    def undo(self):
        self.say(undo.undo_last()[1])

    def view_log(self):
        self.out.delete("1.0", "end")
        for line in logger.read_recent(40) or ["Log is empty."]:
            self.say(line)


def run(folder=""):
    root = tk.Tk()
    App(root, folder)
    root.mainloop()


if __name__ == "__main__":
    run()
