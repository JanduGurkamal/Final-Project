import tkinter as tk
import json
import random
import sys
import main_for_desk
import time
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QFrame,
                             QWidget, QStackedWidget, QLineEdit, QTextEdit, QInputDialog, QDialog, QDateEdit, QTimeEdit,
                             QMessageBox)
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation, QDate, QTime, QSize


class AddContactDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add Contact")
        self.setGeometry(100, 100, 300, 200)

        layout = QVBoxLayout()

        self.first_name_label = QLabel("First Name:")
        self.first_name_input = QLineEdit()
        layout.addWidget(self.first_name_label)
        layout.addWidget(self.first_name_input)

        self.email_label = QLabel("Email:")
        self.email_input = QLineEdit()
        layout.addWidget(self.email_label)
        layout.addWidget(self.email_input)

        self.submit_button = QPushButton("Submit")
        self.submit_button.setStyleSheet("background-color: #88c0d0; color: #2e3440; padding: 10px;")
        self.submit_button.clicked.connect(self.add_contact)
        layout.addWidget(self.submit_button)

        self.setLayout(layout)

    def add_contact(self):
        first_name = self.first_name_input.text()
        email = self.email_input.text()
        if first_name and email:
            contact = {"first_name": first_name, "email": email}
            try:
                with open("emails.json", "r") as file:
                    contacts = json.load(file)
            except FileNotFoundError:
                contacts = []
            contacts.append(contact)
            with open("emails.json", "w") as file:
                json.dump(contacts, file, indent=4)
            self.accept()
        else:
            QMessageBox.warning(self, "Input Error", "Please enter both first name and email.")


class AddUserDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add User")
        self.setGeometry(100, 100, 300, 200)

        layout = QVBoxLayout()

        self.username_label = QLabel("Username:")
        self.username_input = QLineEdit()
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)

        self.password_label = QLabel("Password:")
        self.password_input = QLineEdit()
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)

        self.submit_button = QPushButton("Submit")
        self.submit_button.setStyleSheet("background-color: #88c0d0; color: #2e3440; padding: 10px;")
        self.submit_button.clicked.connect(self.add_user)
        layout.addWidget(self.submit_button)

        self.setLayout(layout)

    def add_user(self):
        username = self.username_input.text()
        password = self.password_input.text()
        if username and password:
            connection_id = str(random.randint(10000, 99999))
            user = {"username": username, "password": password, "connection_id": connection_id}
            try:
                with open("users.json", "r") as file:
                    users = json.load(file)
            except FileNotFoundError:
                users = []
            users.append(user)
            with open("users.json", "w") as file:
                json.dump(users, file, indent=4)
            self.accept()
        else:
            QMessageBox.warning(self, "Input Error", "Please enter both username and password.")


class DeleteUserDialog(QDialog):
    def __init__(self, username):
        super().__init__()
        self.username = username
        self.setWindowTitle("Delete User")
        self.setGeometry(100, 100, 300, 150)

        layout = QVBoxLayout()
        self.confirm_label = QLabel(f"Are you sure you want to delete user {self.username}?")
        layout.addWidget(self.confirm_label)

        self.confirm_button = QPushButton("Yes, Delete")
        self.confirm_button.setStyleSheet("background-color: #bf616a; color: #2e3440; padding: 10px;")
        self.confirm_button.clicked.connect(self.delete_user)
        layout.addWidget(self.confirm_button)

        self.setLayout(layout)

    def delete_user(self):
        try:
            with open("users.json", "r") as file:
                users = json.load(file)
            users = [user for user in users if user["username"] != self.username]
            with open("users.json", "w") as file:
                json.dump(users, file, indent=4)
            self.accept()
        except FileNotFoundError:
            pass


class MainWindow(QMainWindow):
    c=0
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Futuristic Virtual Assistant")
        self.setGeometry(100, 100, 1024, 768)
        self.setStyleSheet("background-color: #2e3440; color: #eceff4;")

        # Central widget
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Main layout
        main_layout = QHBoxLayout(central_widget)

        # Side panel
        side_panel = QFrame(self)
        side_panel.setFixedWidth(250)
        side_panel.setStyleSheet("background-color: #3b4252;")
        side_layout = QVBoxLayout(side_panel)

        # Add user profile section
        profile_label = QLabel("User Profile", self)
        profile_label.setAlignment(Qt.AlignCenter)
        profile_label.setFont(QFont("Open Sans", 16))
        profile_label.setStyleSheet("color: #eceff4;")
        side_layout.addWidget(profile_label)

        # Add buttons to side panel
        button1 = QPushButton("Settings", self)
        button1.setFont(QFont("Roboto", 14))
        button1.setStyleSheet("background-color: #4c566a; color: #88c0d0; border: none; padding: 15px;")
        button1.setCursor(Qt.PointingHandCursor)
        button1.clicked.connect(self.show_settings)
        side_layout.addWidget(button1)

        button2 = QPushButton("Logs", self)
        button2.setFont(QFont("Roboto", 14))
        button2.setStyleSheet("background-color: #4c566a; color: #88c0d0; border: none; padding: 15px;")
        button2.setCursor(Qt.PointingHandCursor)
        button2.clicked.connect(self.show_logs)
        side_layout.addWidget(button2)

        button3 = QPushButton("Home", self)
        button3.setFont(QFont("Roboto", 14))
        button3.setStyleSheet("background-color: #4c566a; color: #88c0d0; border: none; padding: 15px;")
        button3.setCursor(Qt.PointingHandCursor)
        button3.clicked.connect(self.show_home)
        side_layout.addWidget(button3)

        # Main content area with QStackedWidget
        self.stack = QStackedWidget(self)
        self.home_widget = QWidget(self)
        self.settings_widget = QWidget(self)
        self.logs_widget = QWidget(self)

        self.stack.addWidget(self.home_widget)
        self.stack.addWidget(self.settings_widget)
        self.stack.addWidget(self.logs_widget)

        # Set up home screen
        home_layout = QVBoxLayout(self.home_widget)
        self.weather_label = QLabel("My Virtual Assistant", self)
        self.weather_label.setAlignment(Qt.AlignCenter)
        self.weather_label.setFont(QFont("Open Sans", 16))
        self.weather_label.setStyleSheet("color: #eceff4;")
        home_layout.addWidget(self.weather_label)

        self.smart_device_label = QLabel("Smart Device Control", self)
        self.smart_device_label.setAlignment(Qt.AlignCenter)
        self.smart_device_label.setFont(QFont("Open Sans", 16))
        self.smart_device_label.setStyleSheet("color: #eceff4;")
        home_layout.addWidget(self.smart_device_label)

        # Add smart device control buttons
        smart_device_layout = QHBoxLayout()
        light_button = QPushButton("Toggle Light", self)
        light_button.setFont(QFont("Roboto", 14))
        light_button.setStyleSheet("background-color: #88c0d0; color: #2e3440; border: none; padding: 15px;")
        light_button.setCursor(Qt.PointingHandCursor)
        light_button.clicked.connect(self.toggle_light)
        smart_device_layout.addWidget(light_button)

        fan_button = QPushButton("Light Off", self)
        fan_button.setFont(QFont("Roboto", 14))
        fan_button.setStyleSheet("background-color: #88c0d0; color: #2e3440; border: none; padding: 15px;")
        fan_button.setCursor(Qt.PointingHandCursor)
        fan_button.clicked.connect(self.toggle_fan)
        smart_device_layout.addWidget(fan_button)

        home_layout.addLayout(smart_device_layout)

        self.events_and_commands_display = QTextEdit(self)
        self.events_and_commands_display.setFont(QFont("Open Sans", 14))
        self.events_and_commands_display.setStyleSheet("color: #2e3440; background-color: #eceff4; padding: 10px;")
        home_layout.addWidget(self.events_and_commands_display)

        # Bottom bar with Exit and Voice Command buttons
        bottom_bar = QFrame(self)
        bottom_bar.setFixedHeight(100)
        bottom_bar.setStyleSheet("background-color: #3b4252;")
        bottom_layout = QHBoxLayout(bottom_bar)

        # Add icons to the buttons
        exit_icon_path = "path/to/exit_icon.png"  # Replace with the correct path to the exit icon
        voice_command_icon_path = "path/to/voice_command_icon.png"  # Replace with the correct path to the voice command icon

        self.stop = QPushButton("Exit", self)
        self.stop.setFont(QFont("Open Sans", 14))
        self.stop.setStyleSheet("background-color: #bf616a; color: #2e3440; padding: 15px;")
        self.stop.setIcon(QIcon(exit_icon_path))
        self.stop.setIconSize(QSize(24, 24))
        bottom_layout.addWidget(self.stop)
        self.stop.clicked.connect(self.close)

        self.voice_command_label = QPushButton("Voice Command", self)
        self.voice_command_label.setFont(QFont("Open Sans", 14))
        self.voice_command_label.setStyleSheet("background-color: #88c0d0; color: #2e3440; padding: 15px;")
        self.voice_command_label.setIcon(QIcon(voice_command_icon_path))
        self.voice_command_label.setIconSize(QSize(24, 24))
        bottom_layout.addWidget(self.voice_command_label)
        self.voice_command_label.clicked.connect(self.run)

        home_layout.addWidget(bottom_bar)

        # Add clock to the right side
        clock_layout = QVBoxLayout()
        self.clock_label = QLabel(self)
        self.clock_label.setFont(QFont("Open Sans", 16))
        self.clock_label.setStyleSheet("color: #eceff4; padding: 10px;")
        self.update_clock()
        clock_layout.addWidget(self.clock_label)
        main_layout.addLayout(clock_layout, 1)

        # Add side panel and stack to main layout
        main_layout.addWidget(side_panel)
        main_layout.addWidget(self.stack, 4)

        settings_layout = QVBoxLayout(self.settings_widget)
        settings_label = QLabel("Settings", self)
        settings_label.setAlignment(Qt.AlignCenter)
        settings_label.setFont(QFont("Open Sans", 16))
        settings_label.setStyleSheet("color: #eceff4;")
        settings_layout.addWidget(settings_label)

        add_contact_button = QPushButton("Add Contact", self)
        add_contact_button.setFont(QFont("Roboto", 14))
        add_contact_button.setStyleSheet("background-color: #88c0d0; color: #2e3440; border: none; padding: 15px;")
        add_contact_button.setCursor(Qt.PointingHandCursor)
        add_contact_button.clicked.connect(self.add_contact)
        settings_layout.addWidget(add_contact_button)

        add_user_button = QPushButton("Add User", self)
        add_user_button.setFont(QFont("Roboto", 14))
        add_user_button.setStyleSheet("background-color: #88c0d0; color: #2e3440; border: none; padding: 15px;")
        add_user_button.setCursor(Qt.PointingHandCursor)
        add_user_button.clicked.connect(self.add_user)
        settings_layout.addWidget(add_user_button)

        delete_user_button = QPushButton("Delete User", self)
        delete_user_button.setFont(QFont("Roboto", 14))
        delete_user_button.setStyleSheet("background-color: #bf616a; color: #2e3440; border: none; padding: 15px;")
        delete_user_button.setCursor(Qt.PointingHandCursor)
        delete_user_button.clicked.connect(self.delete_user)
        settings_layout.addWidget(delete_user_button)

        logs_layout = QVBoxLayout(self.logs_widget)
        logs_label = QLabel("Logs", self)
        logs_label.setAlignment(Qt.AlignCenter)
        logs_label.setFont(QFont("Open Sans", 16))
        logs_label.setStyleSheet("color: #eceff4;")
        logs_layout.addWidget(logs_label)

        self.logs_text = QTextEdit(self)
        self.logs_text.setFont(QFont("Open Sans", 14))
        self.logs_text.setStyleSheet("color: #2e3440; background-color: #eceff4; padding: 10px;")
        logs_layout.addWidget(self.logs_text)

    def update_clock(self):
        current_time = time.strftime('%H:%M:%S')
        self.clock_label.setText(current_time)
        QTimer.singleShot(1000, self.update_clock)  # update every second

    def run(self):
        command = main_for_desk.main()
        if isinstance(command, str):  # Ensure the command is a string
            self.events_and_commands_display.append(command)
        else:
            print("Received command is not a string")

    def show_settings(self):
        self.stack.setCurrentWidget(self.settings_widget)

    def show_logs(self):
        self.stack.setCurrentWidget(self.logs_widget)

    def show_home(self):
        self.stack.setCurrentWidget(self.home_widget)

    def toggle_light(self, c):
        response = main_for_desk.send_serial_command('1')
        if response:
            self.events_and_commands_display.append("Light toggled")
        else:
            self.events_and_commands_display.append("Failed to toggle light")

    def toggle_fan(self):
        response = main_for_desk.send_serial_command('0')
        if response:
            self.events_and_commands_display.append("Light toggled")
        else:
            self.events_and_commands_display.append("Failed to toggle light")

    def add_contact(self):
        dialog = AddContactDialog()
        dialog.exec_()
        self.logs_text.append("Contact added")

    def add_user(self):
        dialog = AddUserDialog()
        dialog.exec_()
        self.logs_text.append("User added")

    def delete_user(self):
        username, ok = QInputDialog.getText(self, "Delete User", "Enter username to delete:")
        if ok and username:
            dialog = DeleteUserDialog(username)
            dialog.exec_()
            self.logs_text.append(f"User {username} deleted")


def run():
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())


def check():
    if username_entry.get() == "813958" and password_entry.get() == "1234":
        success = tk.Label(root, text="Connecting...!", font=('Helvetica bold', 16), fg="green", pady=10)
        success.pack()
        root.destroy()
        run()  # Run the PyQt5 application after Tkinter window is destroyed
    else:
        error = tk.Label(root, text="Wrong Connection ID or Password!", font=('Helvetica bold', 16), fg="red", pady=10)
        error.pack()


root = tk.Tk()
root.title("Virtual Assistant")
root.geometry("400x300")

username_label = tk.Label(root, text="Connection ID", font=('Helvetica bold', 20), pady=5)
username_label.pack()
username_entry = tk.Entry(root, font=("Ariel", 18), width=10)
username_entry.pack()

password_label = tk.Label(root, text="Password", font=('Helvetica bold', 20), pady=5)
password_label.pack()
password_entry = tk.Entry(root, show="*", font=("Ariel", 18), width=10)
password_entry.pack()

button = tk.Button(root, text="Connect", command=check, width=10, height=2)
button.pack()

root.mainloop()
