import contextlib
import os
import psutil
from time import sleep
import win32gui
import ctypes
import keyboard

DIABLO_WIN = win32gui.FindWindow("D3 Main Window Class", "Diablo III")


def process_active(name):
    return any(process.name() == name for process in psutil.process_iter())


def kill_process(name):
    for process in psutil.process_iter():
        if process.name() == name:
            print(f"{name}-Process found. Terminating it.")
            process.terminate()
            break


def set_status(diablo_hooked, d3m_paused, listener):
    while True:
        diablo_hooked.setChecked(DIABLO_WIN)
        print(listener.paused)
        d3m_paused.setChecked(listener.paused)
        sleep(0.5)


# Transforms from 1920 x 1080 Base
# Works for all 16 / 9 Resolutions
def transform_coordinates(handle, x, y, rel="left"):
    x1, y1, x2, y2 = win32gui.GetClientRect(handle)  # win32gui.GetWindowRect(handle)
    w = x2 - x1
    h = y2 - y1

    if rel == "left":
        new_x = int((h / 1080) * x)
    elif rel == "right":
        new_x = int(w - (1920 - x) * h / 1080)
    else:
        new_x = int(x * h / 1080 + (w - 1920 * h / 1080) / 2)
    new_y = int((h / 1080) * y)

    return (new_x, new_y)


class AdminStateUnknownError(Exception):
    pass


def user_is_admin():
    with contextlib.suppress(AttributeError):
        return os.getuid() == 0
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() == 1
    except AttributeError as e:
        raise AdminStateUnknownError from e


def hotkey_delete_request(hotkey):
    try:
        scan_codes = keyboard.key_to_scan_codes(hotkey)
        return scan_codes[0] == 83
    except Exception:
        return False


def hotkey_is_numlock(hotkey):
    try:
        scan_code = keyboard.key_to_scan_codes(hotkey)[1]
        return scan_code in [71, 72, 73, 75, 76, 77, 79, 80, 81, 82]
    except Exception:
        return False


def nicer_text(hotkey):
    switcher = {
        82: "Num0",
        79: "Num1",
        80: "Num2",
        81: "Num3",
        75: "Num4",
        76: "Num5",
        77: "Num6",
        71: "Num7",
        72: "Num8",
        73: "Num9",
    }
    return switcher.get(hotkey, hotkey)
