from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTableView


class DataView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.table_view = QTableView()

        layout = QVBoxLayout()
        layout.addWidget(self.table_view)
        self.setLayout(layout)

    def set_model(self, model):
        self.table_view.setModel(model)
