import json


class Settings:
    def __init__(self):
        try:
            with open("./settings.json") as f:
                self.json = json.load(f)
        except Exception:
            self.json = {
                "hotkeys": {
                    "cube_conv_sm": "",
                    "cube_conv_lg": "",
                    "reforge": "",
                    "open_gr": "",
                    "upgrade_gem": "",
                    "leave_game": "",
                    "salvage": "",
                    "gamble": "",
                    "drop_inventory": "",
                    "port_a1": "",
                    "port_a2": "",
                    "port_a3": "",
                    "port_a4": "",
                    "port_a5": "",
                    "lower_difficulty": "",
                    "pause": "f10",
                },
                "special": {
                    "empowered": False,
                    "cube_conv_speed": "normal",
                    "choose_gem": False,
                    "spare_columns": 1,
                    "gamble_item": "ring",
                    "auto_start": False,
                    "auto_open": False,
                    "auto_open_option": "grift",
                    "auto_accept_gr": False,
                    "auto_upgrade_gem": False,
                    "auto_gamble": False,
                },
            }
        self.hotkeys = self.json["hotkeys"]
        self.special = self.json["special"]

    def save(self):
        with open("./settings.json", "w") as f:
            d = {
                "hotkeys": self.hotkeys,
                "special": self.special,
            }
            json.dump(d, f, indent=4)
