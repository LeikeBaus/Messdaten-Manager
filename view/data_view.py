from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTableView


class DataView(QWidget):
    """Display measurement values in a table widget."""

    def __init__(self, parent=None):
        # Build the table container used for measurement previews.
        super().__init__(parent)

        # Bound to MeasurementTableModel by the main window.
        self.table_view = QTableView()

        layout = QVBoxLayout()
        layout.addWidget(self.table_view)
        self.setLayout(layout)

    def set_model(self, model):
        # Bind a Qt table model to the internal table view.
        self.table_view.setModel(model)
