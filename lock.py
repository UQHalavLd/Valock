import tkinter as tk
from tkinter import ttk
import pyautogui
import cv2
import numpy as np
from pynput import keyboard
import time
import requests
from io import BytesIO
from PIL import Image, ImageTk
import sys

# Global değişkenler
running = False
selected_option = None
lock_image = None
whitelist_url = "https://uqhalavld.github.io/valorant-instalock/whitelist.txt"

options = {
    1: {"name": "Astra", "url": "https://uqhalavld.github.io/valorant-instalock/astra.png"},
    2: {"name": "Breach", "url": "https://uqhalavld.github.io/valorant-instalock/breach.png"},
    3: {"name": "Brimstone", "url": "https://uqhalavld.github.io/valorant-instalock/brimstone.png"},
    4: {"name": "Chamber", "url": "https://uqhalavld.github.io/valorant-instalock/chamber.png"},
    5: {"name": "Clove", "url": "https://uqhalavld.github.io/valorant-instalock/clove.png"},
    6: {"name": "Cypher", "url": "https://uqhalavld.github.io/valorant-instalock/cypher.png"},
    7: {"name": "Deadlock", "url": "https://uqhalavld.github.io/valorant-instalock/deadlock.png"},
    8: {"name": "Fade", "url": "https://uqhalavld.github.io/valorant-instalock/fade.png"},
    9: {"name": "Gekko", "url": "https://uqhalavld.github.io/valorant-instalock/gekko.png"},
    10: {"name": "Harbor", "url": "https://uqhalavld.github.io/valorant-instalock/harbor.png"},
    11: {"name": "İso", "url": "https://uqhalavld.github.io/valorant-instalock/iso.png"},
    12: {"name": "Jett", "url": "https://uqhalavld.github.io/valorant-instalock/jett.png"},
    13: {"name": "Kayo", "url": "https://uqhalavld.github.io/valorant-instalock/kayo.png"},
    14: {"name": "Killjoy", "url": "https://uqhalavld.github.io/valorant-instalock/killjoy.png"},
    15: {"name": "Neon", "url": "https://uqhalavld.github.io/valorant-instalock/neon.png"},
    16: {"name": "Omen", "url": "https://uqhalavld.github.io/valorant-instalock/omen.png"},
    17: {"name": "Phoenix", "url": "https://uqhalavld.github.io/valorant-instalock/phoenix.png"},
    18: {"name": "Reyna", "url": "https://uqhalavld.github.io/valorant-instalock/reyna.png"},
    19: {"name": "Raze", "url": "https://uqhalavld.github.io/valorant-instalock/raze.png"},
    20: {"name": "Sage", "url": "https://uqhalavld.github.io/valorant-instalock/sage.png"},
    21: {"name": "Skye", "url": "https://uqhalavld.github.io/valorant-instalock/skye.png"},
    22: {"name": "Sova", "url": "https://uqhalavld.github.io/valorant-instalock/sova.png"},
    23: {"name": "Viper", "url": "https://uqhalavld.github.io/valorant-instalock/viper.png"},
    24: {"name": "Yoru", "url": "https://uqhalavld.github.io/valorant-instalock/yoru.png"},
}

def find_and_click(image, hold=False):
    screenshot = pyautogui.screenshot()
    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

    res = cv2.matchTemplate(screenshot, image, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    if max_val >= 0.9:
        x = max_loc[0] + image.shape[1] // 2
        y = max_loc[1] + image.shape[0] // 2
        if hold:
            pyautogui.mouseDown(x, y)
        else:
            pyautogui.click(x, y)
        return True
    return False

def get_image_from_url(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        img = Image.open(BytesIO(response.content))
        img = img.convert('RGB')
        open_cv_image = np.array(img)
        return cv2.cvtColor(open_cv_image, cv2.COLOR_RGB2BGR)
    except requests.exceptions.RequestException as e:
        print(f"URL hatası: {e}")
    except Image.UnidentifiedImageError:
        print("Resim tanımlanamıyor.")
    except Exception as e:
        print(f"Beklenmedik bir hata oluştu: {e}")
    return None

def check_whitelist(discord_tag):
    try:
        response = requests.get(whitelist_url)
        response.raise_for_status()
        whitelist = response.text.splitlines()
        return discord_tag in whitelist
    except requests.exceptions.RequestException as e:
        print(f"Whitelist kontrol hatası: {e}")
    return False

def task(image):
    global running
    while running:
        if selected_option is not None:
            if find_and_click(image):
                time.sleep(0.5)
                find_and_click(lock_image, hold=True)
                time.sleep(0.5)
                pyautogui.mouseUp()
        time.sleep(0.1)

def on_press(key):
    global running
    if key == keyboard.Key.esc:
        running = False
        print("Durduruldu")

def select_option():
    global selected_option, running
    selected = listbox.curselection()
    if selected:
        option_index = selected[0] + 1
        selected_option = get_image_from_url(options[option_index]["url"])
        print(f"{options[option_index]['name']} seçildi")
        running = True
        task(selected_option)

def preload_images():
    global lock_image
    lock_image = get_image_from_url("https://uqhalavld.github.io/valorant-instalock/kilitle.png")
    if lock_image is not None:
        print("Her şey hazır.")
    else:
        print("Programda sorun oluştu.")

def check_and_start():
    discord_tag = discord_entry.get()
    if check_whitelist(discord_tag):
        whitelist_window.destroy()
        preload_images()
        main_window()
    else:
        error_label.config(text="Whitelist'te değilsiniz.")
        whitelist_window.after(600, sys.exit)

def main_window():
    global listbox, root
    root = tk.Tk()
    root.title("Seçim Ekranı")
    root.geometry("300x400")

    # Simgeyi ayarla
    icon_url = "https://uqhalavld.github.io/valorant-instalock/valo.jpg"
    icon_image = get_image_from_url(icon_url)
    if icon_image is not None:
        icon_image = Image.fromarray(cv2.cvtColor(icon_image, cv2.COLOR_BGR2RGB))
        icon_photo = ImageTk.PhotoImage(icon_image)
        root.iconphoto(False, icon_photo)

    frame = ttk.Frame(root, padding="10")
    frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    listbox = tk.Listbox(frame, height=20)
    for key, value in options.items():
        listbox.insert(tk.END, value["name"])
    listbox.grid(row=0, column=0, padx=10, pady=10)

    select_button = ttk.Button(frame, text="Seç", command=select_option)
    select_button.grid(row=1, column=0, pady=10)

    listener = keyboard.Listener(on_press=on_press)
    listener.start()

    root.mainloop()

def create_whitelist_window():
    global discord_entry, error_label
    window = tk.Tk()
    window.title("Discord İsim Etiketi Kontrolü")
    window.geometry("400x200")

    ttk.Label(window, text="Discord İsim Etiketi (Örn: denemehesabı123.):").pack(pady=10)
    discord_entry = ttk.Entry(window, width=30)
    discord_entry.pack(pady=10)

    check_button = ttk.Button(window, text="Kontrol Et", command=check_and_start)
    check_button.pack(pady=10)

    error_label = ttk.Label(window, text="", foreground="red")
    error_label.pack(pady=10)

    return window

# Whitelist penceresini oluştur ve göster
whitelist_window = create_whitelist_window()
whitelist_window.mainloop()
