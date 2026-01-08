# 1s_system_termux.py
import os
import shutil
import time
import schedule
from pathlib import Path
import subprocess

# ==========================
# CONFIGURATION (Termux-friendly)
# ==========================
# Termux storage path
BASE_DIR = "/storage/emulated/0/1s_system"  # Make sure this folder exists
WASTE_EXTENSIONS = [".tmp", ".log", ".bak"]  # Files to delete automatically
PDF_EXTENSIONS = [".pdf"]

# Folders for each name
NAMES = ["Rudra", "Ludovico", "Sample"]  # Add names as needed

# GitHub repo path (if you want auto-sync)
GIT_REPO_DIR = BASE_DIR  # Assuming repo is cloned here

# ==========================
# FUNCTIONS
# ==========================
def create_folders():
    """Create folders for each name if not exist"""
    for name in NAMES:
        folder_path = os.path.join(BASE_DIR, name)
        os.makedirs(folder_path, exist_ok=True)

def organize_files():
    """Move PDFs to the correct folders based on naming"""
    for file in os.listdir(BASE_DIR):
        file_path = os.path.join(BASE_DIR, file)
        if os.path.isfile(file_path) and any(file_path.endswith(ext) for ext in PDF_EXTENSIONS):
            for name in NAMES:
                if name.lower() in file.lower():
                    target_path = os.path.join(BASE_DIR, name, file)
                    if not os.path.exists(target_path):  # Avoid overwrite
                        shutil.move(file_path, target_path)
                    break

def delete_waste():
    """Delete unwanted files automatically"""
    for file in os.listdir(BASE_DIR):
        file_path = os.path.join(BASE_DIR, file)
        if os.path.isfile(file_path) and any(file.endswith(ext) for ext in WASTE_EXTENSIONS):
            os.remove(file_path)

def github_sync():
    """Push changes to GitHub (optional)"""
    try:
        subprocess.run(["git", "-C", GIT_REPO_DIR, "add", "."], check=True)
        subprocess.run(["git", "-C", GIT_REPO_DIR, "commit", "-m", "Auto-update 1s System"], check=True)
        subprocess.run(["git", "-C", GIT_REPO_DIR, "push", "origin", "main"], check=True)
    except subprocess.CalledProcessError:
        pass  # No changes or errors are ignored

def run_all():
    create_folders()
    delete_waste()
    organize_files()
    github_sync()

# ==========================
# AUTO-UPDATE & UPGRADE FUNCTION
# ==========================
def self_update():
    """Pull latest code from GitHub and restart"""
    try:
        subprocess.run(["git", "-C", GIT_REPO_DIR, "pull"], check=True)
    except subprocess.CalledProcessError:
        pass  # If no updates or fail, continue

# ==========================
# SCHEDULE TASKS
# ==========================
# Run file management every 10 minutes
schedule.every(10).minutes.do(run_all)

# Pull updates from GitHub every hour
schedule.every().hour.do(self_update)

# First run immediately
run_all()
self_update()

# Continuous loop
while True:
    schedule.run_pending()
    time.sleep(1)
