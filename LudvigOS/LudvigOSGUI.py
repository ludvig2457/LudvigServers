import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton

class LudvigOSGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("LudvigOS GUI")
        self.setGeometry(200, 200, 400, 200)

        layout = QVBoxLayout()

        # Заголовок
        self.label = QLabel("Welcome to LudvigOS GUI")
        layout.addWidget(self.label)

        # Кнопка возврата в bash
        self.button = QPushButton("Switch to Bash")
        self.button.clicked.connect(self.close)  # Закрываем GUI → возврат в CLI
        layout.addWidget(self.button)

        self.setLayout(layout)

def main():
    app = QApplication(sys.argv)
    window = LudvigOSGUI()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
