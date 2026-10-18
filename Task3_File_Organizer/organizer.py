#!/usr/bin/env python3
"""Automated File Organizer & Cleanup Utility

Scans a folder (e.g. Downloads), sorts every file into category subfolders
(Documents, Images, Videos, Audio, Archives, Code, Others) based on its
extension, and handles naming collisions and permission errors safely.
Every action is logged to the console and to 'organizer.log'.

Usage:
    python organizer.py                      # asks for a folder (default: ~/Downloads)
    python organizer.py "C:/Users/me/Downloads"
    python organizer.py ./messy_folder --dry-run   # preview only, nothing moved
    python organizer.py ./messy_folder --yes       # skip the confirmation prompt
"""

import argparse
import logging
import os
import shutil
from collections import Counter
from pathlib import Path

EXTENSION_MAP = {
    "Documents": {".pdf", ".doc", ".docx", ".txt", ".rtf", ".odt", ".xls", ".xlsx",
                  ".csv", ".ppt", ".pptx", ".md"},
    "Images": {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp", ".tiff", ".ico"},
    "Videos": {".mp4", ".mkv", ".avi", ".mov", ".wmv", ".flv", ".webm"},
    "Audio": {".mp3", ".wav", ".aac", ".flac", ".ogg", ".m4a"},
    "Archives": {".zip", ".rar", ".7z", ".tar", ".gz", ".bz2"},
    "Code": {".py", ".js", ".html", ".css", ".java", ".c", ".cpp", ".h", ".json",
             ".xml", ".sql", ".sh", ".ts"},
}
DEFAULT_CATEGORY = "Others"
LOG_FILE = Path(__file__).resolve().parent / "organizer.log"

logger = logging.getLogger("organizer")


def setup_logging():
    logger.setLevel(logging.INFO)
    logger.handlers.clear()
    fmt = logging.Formatter("%(asctime)s | %(levelname)-7s | %(message)s", "%H:%M:%S")
    for handler in (logging.StreamHandler(), logging.FileHandler(LOG_FILE, encoding="utf-8")):
        handler.setFormatter(fmt)
        logger.addHandler(handler)


def get_category(filename):
    """Return the category folder name for a file based on its extension."""
    ext = Path(filename).suffix.lower()
    for category, extensions in EXTENSION_MAP.items():
        if ext in extensions:
            return category
    return DEFAULT_CATEGORY


def unique_destination(dest):
    """If dest exists, return 'name (1).ext', 'name (2).ext', ... (no overwrite)."""
    if not dest.exists():
        return dest
    counter = 1
    while True:
        candidate = dest.with_name(f"{dest.stem} ({counter}){dest.suffix}")
        if not candidate.exists():
            return candidate
        counter += 1


def organize(folder, dry_run=False):
    """Move files in `folder` into category subfolders. Returns a stats dict."""
    stats = {"moved": Counter(), "skipped": 0, "errors": 0, "renamed": 0}
    script_name = Path(__file__).name

    with os.scandir(folder) as entries:
        files = [e for e in entries if e.is_file(follow_symlinks=False)]

    for entry in sorted(files, key=lambda e: e.name.lower()):
        if entry.name.startswith(".") or entry.name in (script_name, LOG_FILE.name):
            stats["skipped"] += 1
            continue

        category = get_category(entry.name)
        target_dir = Path(folder) / category
        destination = unique_destination(target_dir / entry.name)
        if destination.name != entry.name:
            stats["renamed"] += 1
            logger.warning("Name collision: '%s' -> '%s'", entry.name, destination.name)

        if dry_run:
            logger.info("[DRY RUN] %s -> %s/", entry.name, category)
            stats["moved"][category] += 1
            continue

        try:
            target_dir.mkdir(exist_ok=True)
            shutil.move(entry.path, str(destination))
            logger.info("Moved: %s -> %s/", entry.name, category)
            stats["moved"][category] += 1
        except PermissionError:
            logger.error("Permission denied (file in use or protected): %s", entry.name)
            stats["errors"] += 1
        except FileExistsError:
            logger.error("File already exists, skipped: %s", entry.name)
            stats["errors"] += 1
        except OSError as err:
            logger.error("Could not move %s: %s", entry.name, err)
            stats["errors"] += 1
    return stats


def print_summary(stats, folder, dry_run):
    total = sum(stats["moved"].values())
    line = "=" * 40
    print(f"\n{line}\n  EXECUTION SUMMARY {'(DRY RUN)' if dry_run else ''}\n{line}")
    print(f"  Folder           : {folder}")
    print(f"  Files {'to move' if dry_run else 'relocated':<10}: {total}")
    for category, count in sorted(stats["moved"].items()):
        print(f"      {category:<12} {count}")
    print(f"  Renamed (collide): {stats['renamed']}")
    print(f"  Skipped          : {stats['skipped']}")
    print(f"  Errors           : {stats['errors']}")
    print(f"  Log file         : {LOG_FILE.name}\n{line}")


def parse_args():
    parser = argparse.ArgumentParser(description="Organize a folder into category subfolders.")
    parser.add_argument("folder", nargs="?", help="folder to organize (default: ask)")
    parser.add_argument("--dry-run", action="store_true", help="preview without moving files")
    parser.add_argument("-y", "--yes", action="store_true", help="skip confirmation prompt")
    return parser.parse_args()


def main():
    args = parse_args()
    setup_logging()

    folder = args.folder
    if not folder:
        default = str(Path.home() / "Downloads")
        folder = input(f"Folder to organize [{default}]: ").strip().strip('"') or default
    folder = Path(folder).expanduser().resolve()

    if not folder.is_dir():
        logger.error("Not a valid folder: %s", folder)
        return

    if not args.dry_run and not args.yes:
        answer = input(f"This will move files inside '{folder}'. Continue? (y/n): ").strip().lower()
        if answer != "y":
            print("Cancelled. No files were changed.")
            return

    logger.info("Organizing: %s", folder)
    stats = organize(folder, dry_run=args.dry_run)
    print_summary(stats, folder, args.dry_run)


if __name__ == "__main__":
    main()
