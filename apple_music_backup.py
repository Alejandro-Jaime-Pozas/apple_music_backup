#!/usr/bin/env python3

import os
import shutil
import time
from datetime import datetime
import subprocess
from pathlib import Path

# Configuration
APPLE_MUSIC_LIBRARY_PATH = os.path.expanduser("~/Music/Apple Music Main/Music Library iTunes Main.musiclibrary")
# ONEDRIVE_BACKUP_DIR = os.path.expanduser("~/OneDrive/Music/Apple Music library backup")
ONEDRIVE_BACKUP_DIR = os.path.expanduser("~/Music/Backups")
MAX_BACKUPS = 25

def is_apple_music_running():
    """Check if Apple Music is running using ps command"""
    try:
        output = subprocess.check_output(["ps", "aux"]).decode()
        return "Music.app" in output
    except subprocess.CalledProcessError:
        return False

def create_backup():
    """Create a backup of the Apple Music library file"""
    # Create backup directory if it doesn't exist
    os.makedirs(ONEDRIVE_BACKUP_DIR, exist_ok=True)

    # Generate backup filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_filename = f"Music_Library_{timestamp}.musiclibrary"
    backup_path = os.path.join(ONEDRIVE_BACKUP_DIR, backup_filename)

    # Copy the library file
    try:
        # Use copy2 to preserve metadata
        shutil.copy2(APPLE_MUSIC_LIBRARY_PATH, backup_path)
        print(f"Backup created successfully: {backup_filename}")

        # Clean up old backups if needed
        cleanup_old_backups()

    except FileNotFoundError:
        print(f"Error: Could not find the Apple Music library file at {APPLE_MUSIC_LIBRARY_PATH}")
    except PermissionError:
        print("Error: Permission denied. Make sure you have the necessary permissions to access the files.")
    except Exception as e:
        print(f"Error creating backup: {e}")

def cleanup_old_backups():
    """Remove oldest backups if we have more than MAX_BACKUPS"""
    backups = sorted(Path(ONEDRIVE_BACKUP_DIR).glob("*.musiclibrary"))

    if len(backups) > MAX_BACKUPS:
        # Remove oldest backups
        for old_backup in backups[:-MAX_BACKUPS]:
            try:
                shutil.rmtree(old_backup)
                print(f"Removed old backup: {old_backup.name}")
            except Exception as e:
                print(f"Error removing old backup {old_backup.name}: {e}")

def main():
    print("Starting Apple Music backup monitor...")
    print(f"Monitoring: {APPLE_MUSIC_LIBRARY_PATH}")
    print(f"Backup directory: {ONEDRIVE_BACKUP_DIR}")

    was_running = is_apple_music_running()

    while True:
        is_running = is_apple_music_running()

        # If Apple Music was running but now isn't, create a backup
        if was_running and not is_running:
            print("Apple Music closed, creating backup...")
            create_backup()

        was_running = is_running
        time.sleep(10)  # Check every 10 seconds

if __name__ == "__main__":
    main()
