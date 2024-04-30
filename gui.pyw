from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QTabWidget,
    QGridLayout,
    QCheckBox,
    QGroupBox,
    QLabel,
    QPushButton,
    QRadioButton,
    QMessageBox,
    QListWidget,
    QListWidgetItem,
    QSpinBox,
    QDesktopWidget,
    QDialog,
)
from PyQt5 import QtCore
from PyQt5.QtGui import QIcon
import sys
import os
import string
import keyboard
import Style.windows as windows
from utils import hotkey_delete_request, hotkey_is_numlock, nicer_text
from utils import DIABLO_WIN
import resources
from time import sleep
from settings import Settings
from listener import Listener
from kthread import KThread


try:
    wd = sys._MEIPASS
except AttributeError:
    wd = ""


class MainWindow(QMainWindow):
    def __init__(self, settings, listener):
        super().__init__()
        self.settings = settings
        self.listener = listener
        self.setWindowTitle("D3M")
        self.table_widget = TableWidget(self)
        self.setCentralWidget(self.table_widget)
        self.locate_to_center()

        self.status_thread = KThread(target=self.set_status)
        self.status_thread.start()

    def locate_to_center(self):
        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())

    def set_status(self):
        while True:
            self.table_widget.diablo_hooked.setChecked(DIABLO_WIN)
            sleep(1)

    def closeEvent(self, event):
        self.settings.save()
        self.listener.thread.terminate()
        self.status_thread.terminate()
        sys.stdout = sys.__stdout__
        super().closeEvent(event)


class TableWidget(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.settings = parent.settings
        self.listener = parent.listener
        self.layout = QGridLayout(self)

        self.tabs = QTabWidget()
        self.hotkey_tab = HotkeyTab(parent)

        self.tabs.addTab(self.hotkey_tab, "Hotkeys")
        self.layout.addWidget(self.tabs, 0, 0, 1, 3)

        self.diablo_hooked = QCheckBox(self)
        self.diablo_hooked.setText("Diablo hooked")
        self.diablo_hooked.setDisabled(True)
        self.layout.addWidget(self.diablo_hooked, 2, 0)

        self.d3m_paused = QCheckBox(self)
        self.d3m_paused.setText("D3M paused")
        self.d3m_paused.setDisabled(True)
        self.layout.addWidget(self.d3m_paused, 2, 1)
        self.listener.gui_paused = self.d3m_paused

        label = QLabel(self)
        label.setText('<a href="https://github.com/VocalTrance/Eule.py">Github Credits</a>')
        label.setOpenExternalLinks(True)
        self.layout.addWidget(label, 2, 2)

        self.setLayout(self.layout)


class HotkeyTab(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.layout = QGridLayout(self)
        self.settings = parent.settings
        self.listener = parent.listener

        self.buttons = {}

        general = QGroupBox(self)
        general_layout = QGridLayout(general)
        general.setTitle("General")
        self.layout.addWidget(general, 0, 0)

        ######################

        label = QLabel(general)
        label.setText("Pause Macros")
        general_layout.addWidget(label, 0, 0)
        button = QPushButton(general)
        self.buttons["pause"] = button
        button.setText(nicer_text(self.settings.hotkeys["pause"]))
        button.clicked.connect(lambda: self.set_hotkey("pause"))
        general_layout.addWidget(button, 0, 1)

        label = QLabel(general)
        label.setText("Leave Game")
        general_layout.addWidget(label, 1, 0)
        button = QPushButton(general)
        self.buttons["leave_game"] = button
        button.setText(nicer_text(self.settings.hotkeys["leave_game"]))
        button.clicked.connect(lambda: self.set_hotkey("leave_game"))
        general_layout.addWidget(button, 1, 1)

        label = QLabel(general)
        label.setText("Normalize Difficulty")
        general_layout.addWidget(label, 2, 0)
        button = QPushButton(general)
        self.buttons["lower_difficulty"] = button
        button.setText(nicer_text(self.settings.hotkeys["lower_difficulty"]))
        button.clicked.connect(lambda: self.set_hotkey("lower_difficulty"))
        general_layout.addWidget(button, 2, 1)

        ######################

        porting = QGroupBox(self)
        porting_layout = QGridLayout(porting)
        porting.setTitle("Porting")
        self.layout.addWidget(porting, 1, 0)

        label = QLabel(porting)
        label.setText("Port to A1 Town")
        porting_layout.addWidget(label, 0, 0)
        button = QPushButton(porting)
        self.buttons["port_a1"] = button
        button.setText(nicer_text(self.settings.hotkeys["port_a1"]))
        button.clicked.connect(lambda: self.set_hotkey("port_a1"))
        porting_layout.addWidget(button, 0, 1)

        label = QLabel(porting)
        label.setText("Port to A2 Town")
        porting_layout.addWidget(label, 1, 0)
        button = QPushButton(porting)
        self.buttons["port_a2"] = button
        button.setText(nicer_text(self.settings.hotkeys["port_a2"]))
        button.clicked.connect(lambda: self.set_hotkey("port_a2"))
        porting_layout.addWidget(button, 1, 1)

        label = QLabel(porting)
        label.setText("Port to A3 Town")
        porting_layout.addWidget(label, 2, 0)
        button = QPushButton(porting)
        self.buttons["port_a3"] = button
        button.setText(nicer_text(self.settings.hotkeys["port_a3"]))
        button.clicked.connect(lambda: self.set_hotkey("port_a3"))
        porting_layout.addWidget(button, 2, 1)

        label = QLabel(porting)
        label.setText("Port to A4 Town")
        porting_layout.addWidget(label, 3, 0)
        button = QPushButton(porting)
        self.buttons["port_a4"] = button
        button.setText(nicer_text(self.settings.hotkeys["port_a4"]))
        button.clicked.connect(lambda: self.set_hotkey("port_a4"))
        porting_layout.addWidget(button, 3, 1)

        label = QLabel(porting)
        label.setText("Port to A5 Town")
        porting_layout.addWidget(label, 4, 0)
        button = QPushButton(porting)
        self.buttons["port_a5"] = button
        button.setText(nicer_text(self.settings.hotkeys["port_a5"]))
        button.clicked.connect(lambda: self.set_hotkey("port_a5"))
        porting_layout.addWidget(button, 4, 1)

        ######################

        after_rift = QGroupBox(self)
        after_rift_layout = QGridLayout(after_rift)
        after_rift.setTitle("After Rift")
        self.layout.addWidget(after_rift, 0, 1)

        label = QLabel(after_rift)
        label.setText("Repair & Salvage")
        after_rift_layout.addWidget(label, 0, 0)
        button = QPushButton(after_rift)
        self.buttons["salvage"] = button
        button.setText(nicer_text(self.settings.hotkeys["salvage"]))
        button.clicked.connect(lambda: self.set_hotkey("salvage"))
        after_rift_layout.addWidget(button, 0, 1)

        label = QLabel(after_rift)
        label.setText("Drop Inventory")
        after_rift_layout.addWidget(label, 1, 0)
        button = QPushButton(after_rift)
        self.buttons["drop_inventory"] = button
        button.setText(nicer_text(self.settings.hotkeys["drop_inventory"]))
        button.clicked.connect(lambda: self.set_hotkey("drop_inventory"))
        after_rift_layout.addWidget(button, 1, 1)

        label = QLabel(after_rift)
        label.setText("Spare Columns")
        after_rift_layout.addWidget(label, 2, 0)
        spinbox = QSpinBox(after_rift)
        spinbox.setMinimum(0)
        spinbox.setMaximum(10)
        spinbox.setValue(self.settings.special["spare_columns"])
        spinbox.valueChanged.connect(self.spinbox_changed)
        after_rift_layout.addWidget(spinbox, 2, 1)

        label = QLabel(after_rift)
        label.setText("Gamble")
        after_rift_layout.addWidget(label, 3, 0)
        button = QPushButton(after_rift)
        self.buttons["gamble"] = button
        button.setText(nicer_text(self.settings.hotkeys["gamble"]))
        button.clicked.connect(lambda: self.set_hotkey("gamble"))
        after_rift_layout.addWidget(button, 3, 1)

        ######################

        cube_converter = QGroupBox(self)
        cube_converter_layout = QGridLayout(cube_converter)
        cube_converter.setTitle("Cube Converter")
        self.layout.addWidget(cube_converter, 1, 1)

        label = QLabel(cube_converter)
        label.setText("Reforge / Convert Set")
        cube_converter_layout.addWidget(label, 0, 0, 1, 3)
        button = QPushButton(cube_converter)
        self.buttons["reforge"] = button
        button.setText(nicer_text(self.settings.hotkeys["reforge"]))
        button.clicked.connect(lambda: self.set_hotkey("reforge"))
        cube_converter_layout.addWidget(button, 0, 3, 1, 3)

        label = QLabel(cube_converter)
        label.setText("Convert 1-Slot")
        cube_converter_layout.addWidget(label, 1, 0, 1, 3)
        button = QPushButton(cube_converter)
        self.buttons["cube_conv_sm"] = button
        button.setText(nicer_text(self.settings.hotkeys["cube_conv_sm"]))
        button.clicked.connect(lambda: self.set_hotkey("cube_conv_sm"))
        cube_converter_layout.addWidget(button, 1, 3, 1, 3)

        label = QLabel(cube_converter)
        label.setText("Convert 2-Slot")
        cube_converter_layout.addWidget(label, 2, 0, 1, 3)
        button = QPushButton(cube_converter)
        self.buttons["cube_conv_lg"] = button
        button.setText(nicer_text(self.settings.hotkeys["cube_conv_lg"]))
        button.clicked.connect(lambda: self.set_hotkey("cube_conv_lg"))
        cube_converter_layout.addWidget(button, 2, 3, 1, 3)

        radio = QRadioButton(cube_converter)
        radio.setText("SoL")
        radio.setChecked(self.settings.special["cube_conv_speed"] == "sol")
        radio.clicked.connect(lambda: self.radio_clicked("sol"))
        cube_converter_layout.addWidget(radio, 3, 0, 1, 2)

        radio = QRadioButton(cube_converter)
        radio.setText("Normal")
        radio.setChecked(self.settings.special["cube_conv_speed"] == "normal")
        radio.clicked.connect(lambda: self.radio_clicked("normal"))
        cube_converter_layout.addWidget(radio, 3, 2, 1, 2)

        radio = QRadioButton(cube_converter)
        radio.setText("Slow")
        radio.setChecked(self.settings.special["cube_conv_speed"] == "slow")
        radio.clicked.connect(lambda: self.radio_clicked("slow"))
        cube_converter_layout.addWidget(radio, 3, 4, 1, 2)

        ####################

        greater_rift = QGroupBox(self)
        greater_rift_layout = QGridLayout(greater_rift)
        greater_rift.setTitle("Greater Rift")
        self.layout.addWidget(greater_rift, 0, 2)

        label = QLabel(greater_rift)
        label.setText("Open Grift")
        greater_rift_layout.addWidget(label, 0, 0)
        button = QPushButton(greater_rift)
        self.buttons["open_gr"] = button
        button.setText(nicer_text(self.settings.hotkeys["open_gr"]))
        button.clicked.connect(lambda: self.set_hotkey("open_gr"))
        greater_rift_layout.addWidget(button, 0, 1)

        label = QLabel(greater_rift)
        label.setText("Upgrade Gem")
        greater_rift_layout.addWidget(label, 1, 0)
        button = QPushButton(greater_rift)
        self.buttons["upgrade_gem"] = button
        button.setText(nicer_text(self.settings.hotkeys["upgrade_gem"]))
        button.clicked.connect(lambda: self.set_hotkey("upgrade_gem"))
        greater_rift_layout.addWidget(button, 1, 1)

        checkbox = QCheckBox(greater_rift)
        checkbox.setText("Empowered")
        checkbox.stateChanged.connect(lambda: self.checkbox_clicked("empowered"))
        checkbox.setChecked(self.settings.special["empowered"])
        greater_rift_layout.addWidget(checkbox, 2, 0)

        checkbox = QCheckBox(greater_rift)
        checkbox.setText("Choose Gem to upgrade")
        checkbox.setToolTip("If checked, will upgrade the gem currently selected.")
        checkbox.stateChanged.connect(lambda: self.checkbox_clicked("choose_gem"))
        checkbox.setChecked(self.settings.special["choose_gem"])
        greater_rift_layout.addWidget(checkbox, 2, 1)

        ######################

        gamble_item = QGroupBox(self)
        gamble_item.setTitle("Gamble Item")
        gamble_item_layout = QGridLayout(gamble_item)
        self.layout.addWidget(gamble_item, 1, 2)

        self.gamble_item_list = QListWidget(gamble_item)
        self.gamble_item_list.setSelectionMode(QListWidget.SingleSelection)
        for _item in resources.items():
            item = QListWidgetItem(self.gamble_item_list)
            item.setText(string.capwords(_item.replace("_", " ")))
            item.item = _item
            if _item == self.settings.special["gamble_item"]:
                item.setSelected(True)
        self.gamble_item_list.itemSelectionChanged.connect(self.update_gamble_item)
        gamble_item_layout.addWidget(self.gamble_item_list)

        self.setLayout(self.layout)

    def set_hotkey(self, hotkey):
        self.listener.stop()
        sender = self.sender()
        dialog = AddHotkeyDialog(self)
        dialog.show()
        QApplication.processEvents()
        key_input = keyboard.read_hotkey(suppress=False).upper()
        dialog.close()
        if key_input != "esc":
            if hotkey_delete_request(key_input):
                self.settings.hotkeys[hotkey] = ""
                self.buttons[hotkey].setText("")
            elif hotkey_is_numlock(key_input):
                scan_code = keyboard.key_to_scan_codes(key_input)[1]
                reply = QMessageBox.question(self, "Save Hotkey?", f"New Hotkey: Num{key_input}.\n Save Hotkey?")
                if reply == QMessageBox.Yes:
                    for k, hk in self.settings.hotkeys.items():
                        if hk == scan_code:
                            self.settings.hotkeys[k] = ""
                            self.buttons[k].setText("")
                    self.settings.hotkeys[hotkey] = scan_code
                    sender.setText(f"Num{key_input}")
            else:
                reply = QMessageBox.question(self, "Save Hotkey?", f"New Hotkey: {key_input}.\n Save Hotkey?")
                if reply == QMessageBox.Yes:
                    for k, hk in self.settings.hotkeys.items():
                        if hk == key_input:
                            self.settings.hotkeys[k] = ""
                            self.buttons[k].setText("")
                    self.settings.hotkeys[hotkey] = key_input
                    sender.setText(key_input)

        if not self.listener.paused:
            self.listener.start()
        elif self.settings.hotkeys["pause"]:
            keyboard.add_hotkey(self.settings.hotkeys["pause"], self.listener.pause)

    def checkbox_clicked(self, value):
        self.listener.stop()
        sender = self.sender()
        if value == "empowered":
            settings.special["empowered"] = sender.isChecked()
        elif value == "choose_gem":
            settings.special["choose_gem"] = sender.isChecked()
        elif value == "fast_convert":
            settings.special["fast_convert"] = sender.isChecked()

        if not self.listener.paused:
            self.listener.start()
        elif self.settings.hotkeys["pause"]:
            keyboard.add_hotkey(self.settings.hotkeys["pause"], self.listener.pause)

    def radio_clicked(self, value):
        self.listener.stop()
        if value in ["sol", "normal", "slow"]:
            self.settings.special["cube_conv_speed"] = value

        if not self.listener.paused:
            self.listener.start()
        elif self.settings.hotkeys["pause"]:
            keyboard.add_hotkey(self.settings.hotkeys["pause"], self.listener.pause)

    def spinbox_changed(self):
        self.listener.stop()

        self.settings.special["spare_columns"] = self.sender().value()

        if not self.listener.paused:
            self.listener.start()
        elif self.settings.hotkeys["pause"]:
            keyboard.add_hotkey(self.settings.hotkeys["pause"], self.listener.pause)

    def update_gamble_item(self):
        self.listener.stop()

        selected_item = self.gamble_item_list.selectedItems()[0]
        self.settings.special["gamble_item"] = selected_item.item

        if not self.listener.paused:
            self.listener.start()
        elif self.settings.hotkeys["pause"]:
            keyboard.add_hotkey(self.settings.hotkeys["pause"], self.listener.pause)


class AddHotkeyDialog(QDialog):
    def __init__(self, parent):
        super().__init__()
        self.setWindowTitle("Add new Hotkey")
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.layout = QGridLayout(self)
        label = QLabel(self)
        label.setText("New Hotkey: Enter [Key Combination]")
        self.layout.addWidget(label)

        label = QLabel(self)
        label.setText("Delete Hotkey: Press DELETE")
        self.layout.addWidget(label)

        label = QLabel(self)
        label.setText("Cancel: Press ESC")
        self.layout.addWidget(label)

        self.setLayout(self.layout)


if __name__ == "__main__":
    settings = Settings()
    listener = Listener(settings)
    app = QApplication(sys.argv)
    win = MainWindow(settings, listener)
    mw = windows.ModernWindow(win)

    stylesheet_path = os.path.join(wd, "./Style/frameless.qss")
    icon_path = os.path.join(wd, "./Style/D3M.ico")

    with open(stylesheet_path) as stylesheet:
        mw.setStyleSheet(stylesheet.read())
    mw.setWindowIcon(QIcon(icon_path))

    mw.show()
    sys.exit(app.exec_())
