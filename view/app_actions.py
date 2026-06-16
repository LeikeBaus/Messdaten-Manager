from PyQt6.QtCore import QObject
from PyQt6.QtGui import QAction


class AppActions(QObject):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.experiment_new = QAction("Neues Experiment", self)
        self.experiment_load = QAction("Experiment laden", self)
        self.experiment_save = QAction("Experiment speichern", self)
        self.experiment_delete = QAction("Experiment loeschen", self)

        self.measurement_new = QAction("Neue Messreihe", self)
        self.measurement_import = QAction("Messreihe importieren", self)
        self.measurement_save = QAction("Messreihe speichern", self)
        self.measurement_delete = QAction("Messreihe loeschen", self)

        self.plot_export = QAction("Plot exportieren", self)
