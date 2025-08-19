import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QMenu, QMenuBar, QFrame, QDesktopWidget
)
from PyQt6.QtGui import QIcon, QAction
from PyQt6.QtCore import Qt, QTimer, QTime

class KDEPlasmaSim(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("KDE Plasma - LudvigLinux Simulation")
        self.setGeometry(100, 100, 1280, 720)
        self.setStyleSheet("background-color: #2e3440; color: white;")

        # Центральная область (рабочий стол)
        self.desktop_area = QWidget()
        self.desktop_layout = QVBoxLayout()
        self.desktop_area.setLayout(self.desktop_layout)
        self.setCentralWidget(self.desktop_area)

        # Панель задач
        self.taskbar = QFrame()
        self.taskbar.setFixedHeight(40)
        self.taskbar.setStyleSheet("background-color: #3b4252;")
        self.taskbar_layout = QHBoxLayout()
        self.taskbar.setLayout(self.taskbar_layout)

        # Кнопка меню
        self.start_btn = QPushButton("Menu")
        self.start_btn.setStyleSheet("background-color: #4c566a; color: white; font-weight: bold;")
        self.start_btn.clicked.connect(self.show_menu)
        self.taskbar_layout.addWidget(self.start_btn)

        # Часы
        self.clock_label = QLabel()
        self.clock_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.taskbar_layout.addWidget(self.clock_label)
        self.update_time()
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)

        self.desktop_layout.addWidget(self.taskbar)

        # Меню приложений
        self.menu = QMenu()
        self.menu.addAction(QAction("VS Code", self, triggered=self.launch_vscode))
        self.menu.addAction(QAction("SuperLauncher", self, triggered=self.launch_superlauncher))
        self.menu.addAction(QAction("Terminal", self, triggered=self.launch_terminal))
        self.menu.addAction(QAction("Exit KDE Plasma", self, triggered=self.close))

    def update_time(self):
        self.clock_label.setText(QTime.currentTime().toString("HH:mm:ss"))

    def show_menu(self):
        self.menu.exec(self.start_btn.mapToGlobal(self.start_btn.rect().bottomLeft()))

    def launch_vscode(self):
        import os
        from pathlib import Path
        path = os.path.join(Path(__file__).parent, "apps", "VSCodeSetup.exe")
        if os.path.exists(path):
            os.startfile(path)
        else:
            print("VS Code is not installed. Use 'pacman -S code'.")

    def launch_superlauncher(self):
        import os
        from pathlib import Path
        path = os.path.join(Path(__file__).parent, "apps", "SuperLauncher1.4.0.7.exe")
        if os.path.exists(path):
            os.startfile(path)
        else:
            print("SuperLauncher is not installed. Use 'pacman -S superlauncher'.")

    def launch_terminal(self):
        import subprocess
        subprocess.Popen([sys.executable, os.path.join(Path(__file__).parent, "LudvigOS.py")])

if __name__ == "__main__":
    app = QApplication(sys.argv)
    kde = KDEPlasmaSim()
    kde.show()
    sys.exit(app.exec())
