import json
from datetime import datetime

from pathlib import Path
from PyQt5.QtWidgets import QWidget, QLabel

# from PyQt5.QtCore import QFile, Slot, QObject, Signal
from PyQt5.QtCore import QFile, QObject, pyqtSignal

# from PyQt5.QtUiTools import QUiLoader
from PyQt5 import uic
from PyQt5.QtGui import QPixmap


class UI(QWidget, QObject):
    # config_signal = Signal(str)
    # access_signal = Signal(str)
    config_signal = pyqtSignal(str)
    access_signal = pyqtSignal(str)

    def __init__(self, *args, **kwargs):
        super().__init__(*args)
        self.load_ui()
        self.setWindowTitle("Embedded")
        l_phone = self.findChild(QLabel, "l_phone")
        l_phone.setText(kwargs["phone_number"])
        self._is_swiping = False

        # self.config_signal.connect(self.config_changed)
        # self.access_signal.connect(self.access_changed)
        self.config_signal.connect(self.config_changed)
        self.access_signal.connect(self.access_changed)
        self.config_data = {}
        self.access_data = {}

    # @Slot(str)
    def config_changed(self, payload):
        self.config_data = json.loads(payload)
        for i, comp in enumerate(self.config_data["competencies"]):
            self.add_comp_ui(comp["name"], i)

    # @Slot(str)
    def access_changed(self, payload):
        self.access_data = json.loads(payload)
        status = self.access_data["status"]
        if self.access_data["competencies"]:
            comp = self.access_data["competencies"]
            self._is_swiping = True

            timestamp = self.access_data["timestamp"]
            timestamp = datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d, %H:%M")

            self.change_guide_ui(self.access_data["user_name"], timestamp)

            for idx, c in enumerate(self.config_data["competencies"]):
                if comp[c["id"]]:
                    id = c["id"]
                    st = comp[id]["status"]
                    self.change_compcheck_ui(idx, st)
            self.change_status_ui(status)

        else:
            self._is_swiping = False
            self.change_guide_ui()
            self.change_status_ui()
            for i, c in enumerate(self.config_data["competencies"]):
                self.change_compcheck_ui(i)

    def add_comp_ui(self, name="", index=0):
        w_comp_item = self.findChild(QWidget, f"w_comp_item_{index}")
        l_check = w_comp_item.findChild(QWidget, f"l_check_{index}")
        l_name = w_comp_item.findChild(QWidget, f"l_name_{index}")

        w_comp_item.move(0, 20 * index)
        pixmap = QPixmap("static/default.png")
        l_check.setPixmap(pixmap)
        l_name.setText(name)
        l_check.setStyleSheet("padding-left: 4px;")
        l_name.setStyleSheet("color: #f5f5f5;")

        return w_comp_item

    def change_compcheck_ui(self, index, status=0):
        w_comp_item = self.findChild(QWidget, f"w_comp_item_{index}")
        l_check = w_comp_item.findChild(QWidget, f"l_check_{index}")
        pix_path = ""
        if not self._is_swiping:
            pix_path = "static/default.png"
        elif status == 0:
            pix_path = "static/error.png"
        elif status == 1:
            pix_path = "static/checker.png"
        elif status == 2:
            pix_path = "static/warning.png"
        elif status == 3:
            pix_path = "static/error.png"

        pixmap = QPixmap(pix_path)
        l_check.setPixmap(pixmap)

    def change_status_ui(self, status=0):
        w_comp = self.findChild(QWidget, "w_comp")
        w_status = self.findChild(QWidget, "w_status")
        if self._is_swiping:
            w_comp.move(w_comp.x(), 95)
            w_status.resize(800, 72)
            l_status = w_status.findChild(QLabel, "l_status")
            l_sub = w_status.findChild(QLabel, "l_subtitle")
            l_sub.setText("")
            bg_color = ""
            text = ""

            if status == 0:
                bg_color = "#F45353"
                text = "Expired!"
            elif status == 1:
                bg_color = "#599D43"
                text = "Successful!"
                l_sub.setText("(Please swiping your card again to check out)")
            elif status == 2:
                bg_color = "#E0BA3E"
                text = "Warning!"
            elif status == 3:
                bg_color = "#F45353"
                text = "Failed!"
            w_status.setStyleSheet(f"background-color: {bg_color}")
            l_status.setText(text)
        else:
            w_comp.move(w_comp.x(), 20)
            w_status.resize(800, 0)

    def change_guide_ui(self, username="", timestamp=""):
        l_swiping = self.findChild(QLabel, "l_swiping")
        l_username = self.findChild(QWidget, "l_username")
        l_timestamp = self.findChild(QWidget, "l_timestamp")
        if self._is_swiping:
            l_swiping.setText("")
            l_swiping.lower()
            l_username.setText(f"Welcome {username}")
            l_timestamp.setText(f"(Swiping time: {timestamp})")
        else:
            l_swiping.setText("Swiping your card before using the asset")
            l_swiping.raise_()
            l_username.setText("")
            l_timestamp.setText("")

    def load_ui(self):
        # loader = QUiLoader()
        path = Path(__file__).resolve().parent / "form.ui"
        # ui_file = QFile(path)
        # ui_file.open(QFile.ReadOnly)
        # loader.load(ui_file, self)
        uic.loadUi(path, self)
        # ui_file.close()
