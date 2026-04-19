import sys
import os
import subprocess
import json
import random
import requests
import threading
import websocket
import time

from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout,
    QLineEdit, QPushButton, QLabel
)
from PyQt6.QtCore import Qt

# ---------------- THEME ---------------- #

APP_STYLE = """
QWidget {
    background-color: #0b0b10;
    color: white;
    font-family: Arial;
}

QLabel {
    color: #c084fc;
    font-weight: bold;
}

QLineEdit {
    background-color: #151522;
    border: 1px solid #2a2a35;
    border-radius: 10px;
    padding: 10px;
    color: white;
}

QLineEdit:focus {
    border: 1px solid #a855f7;
}

QPushButton {
    background-color: #7c3aed;
    border-radius: 10px;
    padding: 10px;
    font-weight: bold;
    color: white;
}

QPushButton:hover {
    background-color: #9333ea;
}

QPushButton:pressed {
    background-color: #5b21b6;
}
"""

# ---------------- CONFIG ---------------- #

DEV_MODE = False
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
USERS_FILE = os.path.join(BASE_DIR, "users.json")

ADMIN_IP = "199.101.230.194"

CHAT_SERVER = "ws://199.101.230.194:8000/ws"  # 🔴 CHANGE THIS

verification_store = {}

# ---------------- DATA ---------------- #

def load_data():
    if not os.path.exists(USERS_FILE):
        return {"users": {}, "banned": []}

    with open(USERS_FILE, "r") as f:
        try:
            return json.load(f)
        except:
            return {"users": {}, "banned": []}


def save_data(data):
    with open(USERS_FILE, "w") as f:
        json.dump(data, f, indent=4)


def get_ip():
    try:
        return requests.get("https://api.ipify.org").text.strip()
    except:
        return "unknown"


# ---------------- CHAT ---------------- #

class ChatUI(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Public Chat")
        self.setFixedSize(420, 500)

        self.layout = QVBoxLayout()

        self.chat_log = QLabel("")
        self.chat_log.setWordWrap(True)

        self.status = QLabel("Connecting...")
        self.status.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.input = QLineEdit()
        self.input.setPlaceholderText("Message...")

        self.send_btn = QPushButton("Send")
        self.send_btn.clicked.connect(self.send_message)

        self.layout.addWidget(self.status)
        self.layout.addWidget(self.chat_log)
        self.layout.addWidget(self.input)
        self.layout.addWidget(self.send_btn)

        self.setLayout(self.layout)
        self.setStyleSheet(APP_STYLE)

        self.messages = ""
        self.ws = None
        self.connected = False

        self.start_ws()

    # ---------------- CONNECTION ---------------- #

    def start_ws(self):
        def run():
            while True:
                try:
                    self.ws = websocket.WebSocketApp(
                        CHAT_SERVER,
                        on_message=self.on_message,
                        on_open=self.on_open,
                        on_close=self.on_close,
                        on_error=self.on_error
                    )
                    self.ws.run_forever()
                except:
                    pass

                time.sleep(3)  # auto reconnect

        threading.Thread(target=run, daemon=True).start()

    def on_open(self, ws):
        self.connected = True
        self.status.setText("🟢 Connected")

    def on_close(self, ws, *args):
        self.connected = False
        self.status.setText("🔴 Disconnected")

    def on_error(self, ws, error):
        self.status.setText(f"⚠ Error: {error}")

    def on_message(self, ws, message):
        self.messages += message + "\n"
        self.chat_log.setText(self.messages)

    # ---------------- SEND SAFE ---------------- #

    def send_message(self):
        msg = self.input.text().strip()

        if not msg:
            return

        if not self.connected or not self.ws:
            self.messages += "[NOT CONNECTED]\n"
            self.chat_log.setText(self.messages)
            return

        try:
            self.ws.send(msg)
            self.input.clear()
        except:
            self.messages += "[SEND FAILED]\n"
            self.chat_log.setText(self.messages)


# ---------------- ADMIN ---------------- #

class AdminUI(QWidget):
    def __init__(self, data, save_callback):
        super().__init__()

        self.data = data
        self.save_callback = save_callback

        self.setWindowTitle("Admin Panel")
        self.setFixedSize(340, 320)

        layout = QVBoxLayout()

        self.title = QLabel("ADMIN PANEL")
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Email")

        self.ban_btn = QPushButton("Ban User")
        self.unban_btn = QPushButton("Unban User")
        self.list_btn = QPushButton("List Users")
        self.clear_btn = QPushButton("Clear Users")
        self.dev_btn = QPushButton("Toggle DEV MODE")

        self.status = QLabel("")
        self.status.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.ban_btn.clicked.connect(self.ban_user)
        self.unban_btn.clicked.connect(self.unban_user)
        self.list_btn.clicked.connect(self.list_users)
        self.clear_btn.clicked.connect(self.clear_users)
        self.dev_btn.clicked.connect(self.toggle_dev)

        layout.addWidget(self.title)
        layout.addWidget(self.email_input)
        layout.addWidget(self.ban_btn)
        layout.addWidget(self.unban_btn)
        layout.addWidget(self.list_btn)
        layout.addWidget(self.clear_btn)
        layout.addWidget(self.dev_btn)
        layout.addWidget(self.status)

        self.setLayout(layout)
        self.setStyleSheet(APP_STYLE)

    def ban_user(self):
        email = self.email_input.text().strip()
        if email not in self.data["banned"]:
            self.data["banned"].append(email)
            save_data(self.data)
            self.status.setText("Banned")

    def unban_user(self):
        email = self.email_input.text().strip()
        if email in self.data["banned"]:
            self.data["banned"].remove(email)
            save_data(self.data)
            self.status.setText("Unbanned")

    def list_users(self):
        self.status.setText(", ".join(self.data["users"].keys()))

    def clear_users(self):
        self.data["users"] = {}
        save_data(self.data)
        self.status.setText("Cleared")

    def toggle_dev(self):
        global DEV_MODE
        DEV_MODE = not DEV_MODE
        self.status.setText(f"DEV = {DEV_MODE}")


# ---------------- LOGIN ---------------- #

class AuthUI(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Better Society Login")
        self.setFixedSize(420, 500)

        self.data = load_data()

        layout = QVBoxLayout()

        self.email = QLineEdit()
        self.email.setPlaceholderText("Email")

        self.code = QLineEdit()
        self.code.setPlaceholderText("Code")
        self.code.hide()

        self.send_btn = QPushButton("Send Code")
        self.verify_btn = QPushButton("Verify")
        self.chat_btn = QPushButton("Public Chat")
        self.admin_btn = QPushButton("Admin Panel")

        self.status = QLabel("")

        self.send_btn.clicked.connect(self.send_code)
        self.verify_btn.clicked.connect(self.verify)
        self.chat_btn.clicked.connect(self.open_chat)
        self.admin_btn.clicked.connect(self.open_admin)

        layout.addWidget(self.email)
        layout.addWidget(self.send_btn)
        layout.addWidget(self.code)
        layout.addWidget(self.verify_btn)
        layout.addWidget(self.chat_btn)
        layout.addWidget(self.admin_btn)
        layout.addWidget(self.status)

        self.setLayout(layout)
        self.setStyleSheet(APP_STYLE)

    def send_code(self):
        if DEV_MODE:
            self.launch()
            return

        self.code.show()
        self.status.setText("Code sent")

    def verify(self):
        self.launch()

    def open_chat(self):
        self.chat = ChatUI()
        self.chat.show()

    def open_admin(self):
        self.admin = AdminUI(self.data, save_data)
        self.admin.show()

    def launch(self):
        subprocess.Popen([sys.executable, os.path.join(BASE_DIR, "BetterTool.py")])
        self.close()


# ---------------- RUN ---------------- #

app = QApplication(sys.argv)
window = AuthUI()
window.show()
sys.exit(app.exec())