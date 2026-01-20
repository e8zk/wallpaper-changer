import os
import inquirer
import platform
import ctypes
import time

# Define the path to the folder containing the wallpapers
pathfolder = r"C:\Users\Administrator\Pictures\wallpapers"

# Define the folder variable with the path to the folder
folder = pathfolder

images = [
    f for f in os.listdir(folder) 
    if f.lower().endswith((".jpg", ".jpeg", ".png", ".bmp"))
]

def get_current_wallpaper():
    buffer_size = 512
    current_wallpaper = ctypes.create_unicode_buffer(buffer_size)
    ctypes.windll.user32.SystemParametersInfoW(0x0073, buffer_size, current_wallpaper, 0)
    return current_wallpaper.value
    



def clear_screen():
    """
    Clears the terminal screen based on the current operating system.

    If the operating system is Windows, it will use the "cls" command.
    If the operating system is not Windows, it will use the "clear" command.
    """
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")



if not images:
    raise Exception("No images found in the folder")

while True:
    clear_screen()

    print("Current wallpaper:", os.path.basename(get_current_wallpaper()))
    question = [
        inquirer.List(
            "Wallpaper", 
            message="[↑/↓] Select a wallpaper",
            choices= images + ["← Quit"]
        )
    ]



    answer = inquirer.prompt(question)
    selected = answer["Wallpaper"]



    if answer is None:
        print("Canceled.")
        exit()

    if selected == "← Quit":
        print("Quitting...")
        time.sleep(1.5)
        exit()
        
    full_path = os.path.join(folder, selected)

    ctypes.windll.user32.SystemParametersInfoW(20, 0, full_path, 0)

    print("success, wallpaper changed to {}".format(selected))
    input("Press Enter to continue...")
    clear_screen()

