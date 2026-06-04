from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QMenuBar


class MenuBar(QMenuBar):
    def __init__(self, parent=None):
        super(MenuBar, self).__init__(parent)

        file_menu = self.addMenu("&Datei")
        open_action = QAction("Öffnen", self)
        file_menu.addAction(open_action)
        save_action = QAction("Speichern", self)
        file_menu.addAction(save_action)