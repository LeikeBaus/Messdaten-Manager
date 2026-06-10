from PyQt6.QtWidgets import (
    QDockWidget, QWidget, QVBoxLayout,
    QTreeWidget, QTreeWidgetItem
)
from PyQt6.QtCore import Qt


class SideBar(QDockWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setFeatures(QDockWidget.DockWidgetFeature.NoDockWidgetFeatures)
        self.setAllowedAreas(Qt.DockWidgetArea.LeftDockWidgetArea)

        self.setMaximumWidth(250)
        self.setWindowTitle("Übersicht")

        # Container Widget (wichtig bei QDockWidget)
        container = QWidget()
        layout = QVBoxLayout(container)

        # Tree
        self.experiment_tree = QTreeWidget()
        self.experiment_tree.setHeaderHidden(True)

        # Hauptknoten
        experiments = QTreeWidgetItem(["Temperatur"])

        # Unterpunkte
        QTreeWidgetItem(experiments, ["Messung 1"])
        QTreeWidgetItem(experiments, ["Messung 2"])
        QTreeWidgetItem(experiments, ["Messung 3"])

        self.experiment_tree.addTopLevelItem(experiments)
        experiments.setExpanded(True)

        layout.addWidget(self.experiment_tree)
        self.setWidget(container)