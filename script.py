import os
import inquirer
import platform
import ctypes
import time
import json
import tkinter as tk
from tkinter import filedialog

config_file = "config.json"

def load_config():
    if not os.path.exists(config_file):
        return {}
    with open(config_file, "r") as f:
        return json.load(f)

def save_config(config):
    with open(config_file, "w") as f:
        json.dump(config, f, indent=4)

def pick_folder():
    root = tk.Tk()
    root.withdraw()
    folder = filedialog.askdirectory(title="Select wallpaper folder")
    root.destroy()
    return folder if folder else None

def scan_images(folder):
    return [
        f for f in os.listdir(folder)
        if f.lower().endswith((".jpg", ".jpeg", ".png", ".bmp"))
    ]

def get_current_wallpaper():
    buffer_size = 512
    current_wallpaper = ctypes.create_unicode_buffer(buffer_size)
    ctypes.windll.user32.SystemParametersInfoW(0x0073, buffer_size, current_wallpaper, 0)
    return current_wallpaper.value

def clear_screen():
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")

config = load_config()
folder = config.get("wallpaper_folder")

if not folder or not os.path.isdir(folder):
    print("Select the folder containing the wallpapers.")
    folder = pick_folder()
    if not folder:
        exit()
    config["wallpaper_folder"] = folder
    save_config(config)

while True:
    images = scan_images(folder)
    clear_screen()

    print("Current wallpaper:", os.path.basename(get_current_wallpaper()))

    choices = images + ["Change wallpaper folder", "← Quit"]

    question = [
        inquirer.List(
            "action",
            message="[↑/↓] Select an option",
            choices=choices
        )
    ]

    answer = inquirer.prompt(question)
    if answer is None:
        exit()

    selected = answer["action"]

    if selected == "← Quit":
        print("Quitting...")
        time.sleep(1.5)
        exit()

    if selected == "Change wallpaper folder":
        new_folder = pick_folder()
        if new_folder and os.path.isdir(new_folder):
            folder = new_folder
            config["wallpaper_folder"] = folder
            save_config(config)
        continue

    if selected not in images:
        continue

    full_path = os.path.join(folder, selected)
    ctypes.windll.user32.SystemParametersInfoW(20, 0, full_path, 0)
    input("Press Enter to continue...")
