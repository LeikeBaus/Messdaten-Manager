from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem


class DataWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.table = QTableWidget()

        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["X", "Y"])

        layout = QVBoxLayout()
        layout.addWidget(self.table)
        self.setLayout(layout)

    def set_data(self, x_data, y_data, label_x="X", label_y="Y"):
        # Header setzen
        self.table.setHorizontalHeaderLabels([label_x, label_y])

        # Anzahl Zeilen setzen
        self.table.setRowCount(len(x_data))

        # Daten füllen
        for i in range(len(x_data)):
            self.table.setItem(i, 0, QTableWidgetItem(str(x_data[i])))
            self.table.setItem(i, 1, QTableWidgetItem(str(y_data[i])))