import json
from PyQt6.QtWidgets import QApplication
from view.main_window import MainWindow

def getConfig():
    with open("config.json", "r") as f:
        config = json.load(f)
    return config

def main():
    config = getConfig()
    app = QApplication([])
    window = MainWindow(config)
    window.show()
    app.exec()

if __name__ == "__main__":
    main()