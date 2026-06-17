from PyQt6.QtCore import QAbstractTableModel, QModelIndex, Qt


class MeasurementTableModel(QAbstractTableModel):
    """Expose tabular measurement data to Qt table views."""

    def __init__(self, headers=None, rows=None):
        # Initialize table state with optional startup data.
        super().__init__()
        self._headers = headers or []
        self._rows = rows or []

    def rowCount(self, parent=QModelIndex()):
        # Return visible row count for the current dataset.
        if parent.isValid():
            return 0
        return len(self._rows)

    def columnCount(self, parent=QModelIndex()):
        # Return column count based on headers or first data row.
        if parent.isValid():
            return 0

        if self._headers:
            return len(self._headers)
        if self._rows:
            return len(self._rows[0])
        return 0

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        # Provide cell text for display role requests.
        if not index.isValid():
            return None

        if role == Qt.ItemDataRole.DisplayRole:
            value = self._rows[index.row()][index.column()]
            return str(value)

        return None

    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        # Provide table headers for horizontal and vertical directions.
        if role != Qt.ItemDataRole.DisplayRole:
            return None

        if orientation == Qt.Orientation.Horizontal:
            if section < len(self._headers):
                return self._headers[section]
            return f"Col {section + 1}"

        return str(section + 1)

    def set_measurements(self, headers, rows):
        # begin/endResetModel keeps Qt views in sync with new data.
        self.beginResetModel()
        self._headers = list(headers or [])
        self._rows = list(rows or [])
        self.endResetModel()
