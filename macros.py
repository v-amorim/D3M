import contextlib
import win32api
import win32gui
from time import sleep
from sends import send_mouse, send_key
import keyboard
from utils import transform_coordinates
from utils import DIABLO_WIN
from resources import (
    map_act_coords_by_act,
    map_town_coords_by_act,
    kadala_tab_by_name,
    kadala_item_by_name,
)
from threading import Timer


def cube_conv(speed, is_large_slot):
    item = transform_coordinates(DIABLO_WIN, 1425, 580, rel="right")
    step = transform_coordinates(DIABLO_WIN, 50, 50)
    fill = transform_coordinates(DIABLO_WIN, 710, 840)
    trans = transform_coordinates(DIABLO_WIN, 250, 830)
    bw = transform_coordinates(DIABLO_WIN, 580, 850)
    fw = transform_coordinates(DIABLO_WIN, 850, 850)

    def kanais_cube_conversion(is_large_slot, fill_sleep, trans_sleep, bw_sleep, fw_sleep):
        if is_large_slot:
            iterations = 3
            step_multiplier = 2
        else:
            iterations = 6
            step_multiplier = 1

        for i in range(iterations):
            for j in range(10):
                send_mouse(DIABLO_WIN, "RM", item[0] + j * step[0], item[1] + i * step[1] * step_multiplier)
                macro_sleep(fill_sleep)
                send_mouse(DIABLO_WIN, "LM", fill[0], fill[1])  # Fill
                macro_sleep(trans_sleep)
                send_mouse(DIABLO_WIN, "LM", trans[0], trans[1])  # Transmute
                macro_sleep(bw_sleep)
                send_mouse(DIABLO_WIN, "LM", bw[0], bw[1])  # Backwards
                macro_sleep(fw_sleep)
                send_mouse(DIABLO_WIN, "LM", fw[0], fw[1])  # Forwards

    with contextlib.suppress(StopMacro):
        if speed == "slow":
            kanais_cube_conversion(is_large_slot, 0.13, 0.1, 0.13, 0.1)
        elif speed == "normal":
            kanais_cube_conversion(is_large_slot, 0.13, 0.0, 0.13, 0.0)
        elif speed == "sol":
            kanais_cube_conversion(is_large_slot, 0.06, 0.0, 0.06, 0.0)


def reforge():
    item = transform_coordinates(DIABLO_WIN, 1425, 580, rel="right")
    fill = transform_coordinates(DIABLO_WIN, 710, 840)
    trans = transform_coordinates(DIABLO_WIN, 250, 830)
    bw = transform_coordinates(DIABLO_WIN, 580, 850)
    fw = transform_coordinates(DIABLO_WIN, 850, 850)

    send_mouse(DIABLO_WIN, "RM", item[0], item[1])  # Item
    sleep(0.1)
    send_mouse(DIABLO_WIN, "LM", fill[0], fill[1])  # Fill
    send_mouse(DIABLO_WIN, "LM", trans[0], trans[1])  # Transmute
    sleep(0.1)
    send_mouse(DIABLO_WIN, "LM", bw[0], bw[1])  # Backwards
    send_mouse(DIABLO_WIN, "LM", fw[0], fw[1])  # Forth
    send_mouse(DIABLO_WIN, "RM", item[0], item[1])  # Item


def upgrade_gem(empowered, choose_gem):
    upgrade = transform_coordinates(DIABLO_WIN, 280, 550)

    if not choose_gem:
        first_gem = transform_coordinates(DIABLO_WIN, 100, 640)
        send_mouse(DIABLO_WIN, "LM", first_gem[0], first_gem[1])
        sleep(0.1)
    with contextlib.suppress(StopMacro):
        if not empowered:
            for i in range(4):
                _extracted_from_upgrade_gem_(i, 1, upgrade)
        else:
            for i in range(5):
                _extracted_from_upgrade_gem_(i, 2, upgrade)


# TODO Rename this here and in `upgrade_gem`
def _extracted_from_upgrade_gem_(i, arg1, upgrade):
    if i == arg1:
        send_key(DIABLO_WIN, "t")
    send_mouse(DIABLO_WIN, "LM", upgrade[0], upgrade[1])
    macro_sleep(1.8)


def salvage(spare_columns):
    menu = transform_coordinates(DIABLO_WIN, 517, 480)
    anvil = transform_coordinates(DIABLO_WIN, 165, 295)
    item = transform_coordinates(DIABLO_WIN, 1875, 585, rel="right")
    step = transform_coordinates(DIABLO_WIN, 50, 50)

    send_mouse(DIABLO_WIN, "LM", menu[0], menu[1])  # Salvage Menu
    send_mouse(DIABLO_WIN, "LM", anvil[0], anvil[1])  # Click Salvage Button
    for i in range(6):
        for j in range(10 - spare_columns):
            send_mouse(DIABLO_WIN, "LM", item[0] - j * step[0], item[1] + i * step[1])
            send_key(DIABLO_WIN, "enter")
            send_key(DIABLO_WIN, "enter")
    send_key(DIABLO_WIN, "esc")


def drop_inventory(spare_columns):
    item = transform_coordinates(DIABLO_WIN, 1875, 585, rel="right")
    step = transform_coordinates(DIABLO_WIN, 50, 50)
    x, y = win32gui.ScreenToClient(DIABLO_WIN, win32api.GetCursorPos())

    send_key(DIABLO_WIN, "c")
    for i in range(6):
        for j in range(10 - spare_columns):
            send_mouse(DIABLO_WIN, "LM", item[0] - j * step[0], item[1] + i * step[1])
            send_mouse(DIABLO_WIN, "LM", x, y)
    send_key(DIABLO_WIN, "c")


def open_gr():
    grift = transform_coordinates(DIABLO_WIN, 270, 480)
    accept = transform_coordinates(DIABLO_WIN, 260, 850)

    send_mouse(DIABLO_WIN, "LM", grift[0], grift[1])
    send_mouse(DIABLO_WIN, "LM", accept[0], accept[1])


def open_rift():
    rift = transform_coordinates(DIABLO_WIN, 270, 300)
    accept = transform_coordinates(DIABLO_WIN, 260, 850)

    send_mouse(DIABLO_WIN, "LM", rift[0], rift[1])
    send_mouse(DIABLO_WIN, "LM", accept[0], accept[1])


def leave_game():
    leave = transform_coordinates(DIABLO_WIN, 230, 475)

    send_key(DIABLO_WIN, "esc")
    send_mouse(DIABLO_WIN, "LM", leave[0], leave[1])


def port_town(act):
    act_coords = map_act_coords_by_act(act)
    town_coords = map_town_coords_by_act(act)

    bw_map = transform_coordinates(DIABLO_WIN, 895, 125, rel="middle")
    act = transform_coordinates(DIABLO_WIN, act_coords[0], act_coords[1], rel="middle")
    town = transform_coordinates(DIABLO_WIN, town_coords[0], town_coords[1], rel="middle")

    send_key(DIABLO_WIN, "m")
    send_mouse(DIABLO_WIN, "LM", bw_map[0], bw_map[1])
    send_mouse(DIABLO_WIN, "LM", act[0], act[1])
    send_mouse(DIABLO_WIN, "LM", town[0], town[1])


def lower_difficulty():
    lower = transform_coordinates(DIABLO_WIN, 1700, 400, rel="right")

    send_key(DIABLO_WIN, "esc")
    for _ in range(19):
        send_mouse(DIABLO_WIN, "LM", lower[0], lower[1])
        send_key(DIABLO_WIN, "enter")
    send_key(DIABLO_WIN, "esc")


def gamble(item):
    tab_coords = kadala_tab_by_name(item)
    item_coords = kadala_item_by_name(item)
    tab = transform_coordinates(DIABLO_WIN, tab_coords[0], tab_coords[1])
    item = transform_coordinates(DIABLO_WIN, item_coords[0], item_coords[1])

    send_mouse(DIABLO_WIN, "LM", tab[0], tab[1])
    for _ in range(60):
        send_mouse(DIABLO_WIN, "RM", item[0], item[1])


# cant pause this via the regular pause hotkey for now
is_running = False
timers = []


class StopMacro(Exception):
    pass


def macro_sleep(time):
    for _ in range(int(time * 100)):
        if keyboard.is_pressed("esc"):
            raise StopMacro
        else:
            sleep(0.008)


class RepeatedTimer(object):
    def __init__(self, interval, function, *args, **kwargs):
        self._timer = None
        self.interval = interval
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.is_running = False

    def _run(self):
        self.is_running = False
        self.start()
        self.function(*self.args, **self.kwargs)

    def start(self):
        if not self.is_running:
            self._timer = Timer(self.interval, self._run)
            self._timer.start()
            self.is_running = True

    def stop(self):
        self._timer.cancel()
        self.is_running = False
        print("stopping timers")
