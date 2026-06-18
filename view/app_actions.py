from PyQt6.QtCore import QObject
from PyQt6.QtGui import QAction


class AppActions(QObject):
    """Bundle QAction objects shared by menu and toolbar."""

    def __init__(self, parent=None):
        # Create all user-triggerable actions in one place.
        super().__init__(parent)

        # Central action registry shared by menu and toolbar.
        self.experiment_new = QAction("Neues Experiment", self)
        self.experiment_load = QAction("Experiment laden", self)
        self.experiment_save = QAction("Experiment speichern", self)
        self.experiment_delete = QAction("Experiment loeschen", self)

        self.measurement_new = QAction("Neue Messreihe", self)
        self.measurement_import = QAction("Messreihe importieren", self)
        self.measurement_save = QAction("Messreihe speichern", self)
        self.measurement_delete = QAction("Messreihe loeschen", self)

        self.plot_export = QAction("Plot exportieren", self)
        self.copy_plot_action = QAction("Copy Plot to Clipboard", self)
        self.copy_plot_action.triggered.connect(self._on_copy_plot)
