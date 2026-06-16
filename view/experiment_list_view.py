from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QAbstractItemView, QDockWidget, QTreeView


class ExperimentListView(QDockWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setFeatures(QDockWidget.DockWidgetFeature.NoDockWidgetFeatures)
        self.setAllowedAreas(Qt.DockWidgetArea.LeftDockWidgetArea)
        self.setMaximumWidth(250)
        self.setWindowTitle("Übersicht")

        self.tree_view = QTreeView(self)
        self.tree_view.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.tree_view.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.setWidget(self.tree_view)

    def set_model(self, model):
        self.tree_view.setModel(model)
        self.tree_view.expandAll()

    def selected_index(self):
        selection_model = self.tree_view.selectionModel()
        if selection_model is None:
            return None

        indexes = selection_model.selectedRows()
        if indexes:
            return indexes[0]

        current_index = self.tree_view.currentIndex()
        if current_index.isValid():
            return current_index

        return None
