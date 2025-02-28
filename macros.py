import contextlib
from time import sleep

import keyboard
import win32api
import win32gui
from resources import (
    DIABLO_WIN,
    kadala_item_by_name,
    kadala_tab_by_name,
    map_act_coords_by_act,
    map_town_coords_by_act,
    send_key,
    send_mouse,
    transform_coordinates,
)


def cube_conv(speed, is_large_slot):
    if not DIABLO_WIN:
        return

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


def reforge():
    item = transform_coordinates(DIABLO_WIN, 1425, 580, rel="right")
    fill = transform_coordinates(DIABLO_WIN, 710, 840)
    trans = transform_coordinates(DIABLO_WIN, 250, 830)
    bw = transform_coordinates(DIABLO_WIN, 580, 850)
    fw = transform_coordinates(DIABLO_WIN, 850, 850)

    send_mouse(DIABLO_WIN, "RM", item[0], item[1])  # Item
    macro_sleep(0.1)
    send_mouse(DIABLO_WIN, "LM", fill[0], fill[1])  # Fill
    send_mouse(DIABLO_WIN, "LM", trans[0], trans[1])  # Transmute
    macro_sleep(0.1)
    send_mouse(DIABLO_WIN, "LM", bw[0], bw[1])  # Backwards
    send_mouse(DIABLO_WIN, "LM", fw[0], fw[1])  # Forth
    send_mouse(DIABLO_WIN, "RM", item[0], item[1])  # Item


def upgrade_gem(empowered, choose_gem):
    upgrade = transform_coordinates(DIABLO_WIN, 280, 550)
    gem_indices = 2 if empowered else 1

    def enchant_loop(times):
        for _ in range(times):
            send_mouse(DIABLO_WIN, "LM", upgrade[0], upgrade[1])
            macro_sleep(1.55)

    if not choose_gem:
        first_gem = transform_coordinates(DIABLO_WIN, 100, 640)
        send_mouse(DIABLO_WIN, "LM", first_gem[0], first_gem[1])
        macro_sleep(0.05)

    with contextlib.suppress(StopMacro):
        enchant_loop(2)
        send_key(DIABLO_WIN, "t")
        enchant_loop(gem_indices + 1)


def salvage(spare_columns):
    menu = transform_coordinates(DIABLO_WIN, 515, 480)
    repair = transform_coordinates(DIABLO_WIN, 515, 615)
    all_items = transform_coordinates(DIABLO_WIN, 260, 600)
    anvil = transform_coordinates(DIABLO_WIN, 165, 295)
    item = transform_coordinates(DIABLO_WIN, 1875, 585, rel="right")
    step = transform_coordinates(DIABLO_WIN, 50, 50)

    send_mouse(DIABLO_WIN, "LM", repair[0], repair[1])  # Repair Menu
    send_mouse(DIABLO_WIN, "LM", all_items[0], all_items[1])  # Click "All Items"
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


class StopMacro(Exception):
    pass


def macro_sleep(time):
    end_time = time.time() + time
    while time.time() < end_time:
        if keyboard.is_pressed("esc"):
            raise StopMacro
        sleep(0.01)
