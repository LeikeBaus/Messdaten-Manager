import json
from PyQt6.QtWidgets import QApplication

from controller.experiment_controller import ExperimentController
from model.experiment_repository import ExperimentRepository
from view.main_window import MainWindow

def getConfig():
    with open("config.json", "r") as f:
        config = json.load(f)
    return config

def main():
    config = getConfig()
    app = QApplication([])
    window = MainWindow(config)
    repository = ExperimentRepository()
    window.controller = ExperimentController(window, repository)
    window.show()
    app.exec()

if __name__ == "__main__":
    main()