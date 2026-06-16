from PyQt6.QtCore import QAbstractListModel, QModelIndex, Qt


class ExperimentListModel(QAbstractListModel):
    def __init__(self, experiments=None):
        super().__init__()
        self._experiments = experiments or []

    def rowCount(self, parent=QModelIndex()):
        if parent.isValid():
            return 0
        return len(self._experiments)

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if not index.isValid():
            return None

        if role == Qt.ItemDataRole.DisplayRole:
            experiment = self._experiments[index.row()]
            title = experiment.metadata.get("title", "")
            return title or experiment.id

        return None

    def set_experiments(self, experiments):
        self.beginResetModel()
        self._experiments = list(experiments)
        self.endResetModel()

    def experiment_at(self, row):
        if row < 0 or row >= len(self._experiments):
            return None
        return self._experiments[row]
