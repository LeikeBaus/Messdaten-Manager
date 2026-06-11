from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QMenuBar

from ..import_dialog import ImportDialog


class MenuBar(QMenuBar):
    def __init__(self, parent=None):
        super(MenuBar, self).__init__(parent)

        file_menu = self.addMenu("&Datei")
        open_action = QAction("Öffnen", self)
        file_menu.addAction(open_action)
        save_action = QAction("Speichern", self)
        file_menu.addAction(save_action)

        import_dialog = ImportDialog()
        import_action = QAction("Importieren", self)
        import_action.triggered.connect(self.open_import_dialog)

        file_menu.addAction(import_action)

    def open_import_dialog(self):
        import_dialog = ImportDialog()
        import_dialog.exec()