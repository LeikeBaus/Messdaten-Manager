from PyQt6.QtCore import QSize
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QToolBar, QStyle


class ToolBar(QToolBar):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setIconSize(QSize(20, 20))
        self.setMovable(False)

        # Icons
        add_laboratory_icon = self.style().standardIcon(QStyle.StandardPixmap.SP_FileDialogNewFolder)
        add_experiment_icon = self.style().standardIcon(QStyle.StandardPixmap.SP_FileIcon)
        save_icon = self.style().standardIcon(QStyle.StandardPixmap.SP_DialogSaveButton)
        del_experiment_icon = self.style().standardIcon(QStyle.StandardPixmap.SP_TrashIcon)

        # Buttons
        # ToDO
        #   - Funktionen der Button Ergänzen
        save_button = QAction(save_icon, "Test", self)
        self.addAction(save_button)

        add_laboratory_button = QAction(add_laboratory_icon, "Add Experiment", self)
        self.addAction(add_laboratory_button)

        add_experiment_button = QAction(add_experiment_icon, "Add Experiment", self)
        self.addAction(add_experiment_button)

        del_experiment_button = QAction(del_experiment_icon, "Delete Experiment", self)
        self.addAction(del_experiment_button)