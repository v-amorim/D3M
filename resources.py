import winsound

import keyboard
import win32api
import win32con
import win32gui

DIABLO_WIN = win32gui.FindWindow("D3 Main Window Class", "Diablo III")


def play_sound(frequency):
    duration = 100
    winsound.Beep(frequency, duration)


def key_to_hex(key):
    switcher = {
        "0": 0x30,
        "1": 0x31,
        "2": 0x32,
        "3": 0x33,
        "4": 0x34,
        "5": 0x35,
        "6": 0x36,
        "7": 0x37,
        "8": 0x38,
        "9": 0x39,
        "a": 0x41,
        "b": 0x42,
        "c": 0x43,
        "d": 0x44,
        "e": 0x45,
        "f": 0x46,
        "g": 0x47,
        "h": 0x48,
        "i": 0x49,
        "j": 0x4A,
        "k": 0x4B,
        "l": 0x4C,
        "m": 0x4D,
        "n": 0x4E,
        "o": 0x4F,
        "p": 0x50,
        "q": 0x51,
        "r": 0x52,
        "s": 0x53,
        "t": 0x54,
        "u": 0x55,
        "v": 0x56,
        "w": 0x57,
        "x": 0x58,
        "y": 0x59,
        "z": 0x5A,
        "enter": 0x0D,
        "esc": 0x1B,
        "space": 0x20,
        "shift": 0x60,
        "alt": 0x12,
    }
    return switcher.get(key, 0x0)


def map_act_coords_by_act(act):
    switcher = {
        1: (740, 620),
        2: (1090, 525),
        3: (710, 400),
        4: (1450, 370),
        5: (590, 550),
    }
    return switcher.get(act, (0, 0))


def map_town_coords_by_act(act):
    switcher = {
        1: (1020, 490),
        2: (1040, 780),
        3: (510, 485),
        4: (515, 745),
        5: (1170, 625),
    }
    return switcher.get(act, (0, 0))


def items():
    return [
        "1-h_weapon",
        "2-h_weapon",
        "quiver",
        "mojo",
        "orb",
        "phylactery",
        "helm",
        "boots",
        "belt",
        "pants",
        "shield",
        "gloves",
        "chest_armor",
        "shoulders",
        "bracers",
        "ring",
        "amulet",
    ]


def kadala_item_by_name(item):
    switcher = {
        **dict.fromkeys(["1-h_weapon", "helm", "ring"], (70, 210)),
        **dict.fromkeys(["quiver", "boots"], (70, 310)),
        **dict.fromkeys(["mojo", "belt"], (70, 410)),
        "pants": (70, 510),
        "shield": (70, 610),
        **dict.fromkeys(["2-h_weapon", "gloves", "amulet"], (290, 210)),
        **dict.fromkeys(["orb", "chest_armor"], (290, 310)),
        **dict.fromkeys(["phylactery", "shoulders"], (290, 410)),
        "bracers": (290, 510),
    }
    return switcher.get(item, (0, 0))


def kadala_tab_by_name(item):
    switcher = {
        **dict.fromkeys(
            ["1-h_weapon", "2-h_weapon", "quiver", "mojo", "orb", "phylactery"],
            (515, 220),
        ),
        **dict.fromkeys(
            [
                "helm",
                "boots",
                "belt",
                "pants",
                "shield",
                "gloves",
                "chest_armor",
                "shoulders",
                "bracers",
            ],
            (515, 350),
        ),
        **dict.fromkeys(["ring", "amulet"], (515, 480)),
    }
    return switcher.get(item, (0, 0))


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


def send_key(handle, key):
    # Check if Diablo III is the active window
    current_window = win32gui.GetForegroundWindow()
    if current_window != handle:
        return
    win32api.PostMessage(handle, win32con.WM_KEYDOWN, key_to_hex(key), 0)
    win32api.PostMessage(handle, win32con.WM_KEYUP, key_to_hex(key), 0)


def send_mouse(handle, key, x, y):
    # Check if Diablo III is the active window
    current_window = win32gui.GetForegroundWindow()
    if current_window != handle:
        return
    lParam = y << 16 | x
    if key == "LM":
        win32api.PostMessage(handle, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, lParam)
        win32api.PostMessage(handle, win32con.WM_LBUTTONUP, 0, lParam)
    elif key == "RM":
        win32api.PostMessage(handle, win32con.WM_RBUTTONDOWN, win32con.MK_RBUTTON, lParam)
        win32api.PostMessage(handle, win32con.WM_RBUTTONUP, 0, lParam)
