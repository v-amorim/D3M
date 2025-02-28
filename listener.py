import sys
from time import sleep

import keyboard
import macros
from kthread import KThread
from resources import play_sound

try:
    wd = sys._MEIPASS
except AttributeError:
    wd = ""


class Listener:
    def __init__(self, settings):
        self.settings = settings
        self.thread = KThread(target=lambda: keyboard.wait("a+r+b+i+t+r+a+r+y"))
        self.thread.start()
        self.start()
        self.thread = KThread(target=self._wait_for_exit)

    def _wait_for_exit(self):
        while True:
            sleep(1)

    def start(self):
        self.paused = False
        hotkeys = self.settings.hotkeys
        special = self.settings.special

        if hotkeys["lower_difficulty"]:
            keyboard.add_hotkey(hotkeys["lower_difficulty"], macros.lower_difficulty, suppress=True)
        if hotkeys["pause"]:
            keyboard.add_hotkey(hotkeys["pause"], self.toggle_pause_resume, suppress=True)
        if hotkeys["port_a1"]:
            keyboard.add_hotkey(hotkeys["port_a1"], macros.port_town, args=(1,), suppress=True)
        if hotkeys["port_a2"]:
            keyboard.add_hotkey(hotkeys["port_a2"], macros.port_town, args=(2,), suppress=True)
        if hotkeys["port_a3"]:
            keyboard.add_hotkey(hotkeys["port_a3"], macros.port_town, args=(3,), suppress=True)
        if hotkeys["port_a4"]:
            keyboard.add_hotkey(hotkeys["port_a4"], macros.port_town, args=(4,), suppress=True)
        if hotkeys["port_a5"]:
            keyboard.add_hotkey(hotkeys["port_a5"], macros.port_town, args=(5,), suppress=True)
        if hotkeys["open_gr"]:
            keyboard.add_hotkey(hotkeys["open_gr"], macros.open_gr, suppress=True)
        if hotkeys["upgrade_gem"]:
            keyboard.add_hotkey(
                hotkeys["upgrade_gem"],
                macros.upgrade_gem,
                args=(special["empowered"], special["choose_gem"]),
            )
        if hotkeys["leave_game"]:
            keyboard.add_hotkey(hotkeys["leave_game"], macros.leave_game, suppress=True)
        if hotkeys["salvage"]:
            keyboard.add_hotkey(
                hotkeys["salvage"],
                macros.salvage,
                args=(special["spare_columns"],),
                suppress=True,
            )
        if hotkeys["drop_inventory"]:
            keyboard.add_hotkey(
                hotkeys["drop_inventory"],
                macros.drop_inventory,
                args=(special["spare_columns"],),
                suppress=True,
            )
        if hotkeys["gamble"]:
            keyboard.add_hotkey(
                hotkeys["gamble"],
                macros.gamble,
                args=(special["gamble_item"],),
                suppress=True,
            )
        if hotkeys["cube_conv_sm"]:
            keyboard.add_hotkey(
                hotkeys["cube_conv_sm"],
                macros.cube_conv,
                args=(special["cube_conv_speed"], False),
            )
        if hotkeys["cube_conv_lg"]:
            keyboard.add_hotkey(
                hotkeys["cube_conv_lg"],
                macros.cube_conv,
                args=(special["cube_conv_speed"], True),
            )
        if hotkeys["reforge"]:
            keyboard.add_hotkey(hotkeys["reforge"], macros.reforge, suppress=True)

    def stop(self):
        keyboard.unhook_all()

    def toggle_pause_resume(self):
        if self.paused:
            keyboard.unhook_all()
            self.start()
            self.gui_paused.setChecked(False)
            play_sound(200)
        else:
            self.activate_pause()
            play_sound(100)
            play_sound(100)

    def activate_pause(self):
        self.paused = True
        self.stop()
        keyboard.add_hotkey(self.settings.hotkeys["pause"], self.toggle_pause_resume, suppress=True)
        self.gui_paused.setChecked(True)
        macros.is_running = False
