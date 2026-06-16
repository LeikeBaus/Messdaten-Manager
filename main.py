import json
from PyQt6.QtWidgets import QApplication

from controller.experiment_controller import ExperimentController
from model.experiment_repository import ExperimentRepository
from view.main_window import MainWindow

def main():
    with open("config.json", "r", encoding="utf-8") as config_file:
        config = json.load(config_file)
    app = QApplication([])
    window = MainWindow(config)
    repository = ExperimentRepository()
    window.controller = ExperimentController(window, repository)
    window.show()
    app.exec()

if __name__ == "__main__":
    main()