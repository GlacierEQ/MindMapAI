import os
import shutil
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox

def organize_and_rename_files(root_dir, excluded_exts, naming_pattern):
    root_path = Path(root_dir)
    destination = root_path / "_organized"
    destination.mkdir(exist_ok=True)

    file_counter = 1

    for filepath in root_path.rglob('*'):
        if filepath.is_file() and filepath.parent != destination:
            ext = filepath.suffix.lower().strip('.')
            if ext in excluded_exts:
                continue

            category_folder = destination / ext
            category_folder.mkdir(exist_ok=True)

            filename_base = filepath.stem[:30]
            new_name = naming_pattern.format(
                num=f"{file_counter:04d}",
                name=filename_base,
                ext=filepath.suffix
            )

            new_path = category_folder / new_name
            shutil.move(str(filepath), str(new_path))  # MOVE instead of copy
            print(f"Moved: {filepath} → {new_path}")
            file_counter += 1

    print("\n✔ All done organizing and moving files.")

def get_user_inputs():
    root = tk.Tk()
    root.withdraw()

    folder_selected = filedialog.askdirectory(title="Select Folder to Organize")
    if not folder_selected:
        messagebox.showerror("Cancelled", "No folder selected.")
        return None, None, None

    exclude_input = simpledialog.askstring(
        "File Type Exclusion",
        "Enter extensions to exclude (comma-separated, e.g., 'exe,iso,mp4'):"
    )
    excluded_exts = [ext.strip().lower() for ext in exclude_input.split(',')] if exclude_input else []

    naming_pattern = simpledialog.askstring(
        "Filename Pattern",
        "Enter naming pattern using {num}, {name}, {ext} (default: '{num}_{name}{ext}')",
        initialvalue="{num}_{name}{ext}"
    ) or "{num}_{name}{ext}"

    return folder_selected, excluded_exts, naming_pattern

if __name__ == "__main__":
    folder, exclude, pattern = get_user_inputs()
    if folder:
        organize_and_rename_files(folder, exclude, pattern)
