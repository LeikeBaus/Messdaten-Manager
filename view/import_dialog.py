from PyQt6.QtWidgets import QDialog, QVBoxLayout, QPushButton, QLabel, QFileDialog, QDialogButtonBox, QLineEdit

class ImportDialog(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Import Messdaten")
        self.setFixedSize(600, 300)

        layout = QVBoxLayout()

        self.label = QLabel("Ausgewählte Datei:")

        self.select_file = QLineEdit()
        self.select_file.setReadOnly(True)

        self.select_file_button = QPushButton("Datei auswählen")
        self.select_file_button.clicked.connect(self.open_file)

        dialog_buttons = QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        self.dialog_box = QDialogButtonBox(dialog_buttons)
        self.dialog_box.accepted.connect(self.accept)
        self.dialog_box.rejected.connect(self.reject)

        layout.addWidget(self.label)
        layout.addWidget(self.select_file)
        layout.addWidget(self.select_file_button)
        layout.addWidget(self.dialog_box)

        self.setLayout(layout)

    def open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Datei auswählen",
            "",
            "Messdateien (*.csv *.json)"
        )

        self.select_file.setText(file_path)

    def selected_file_path(self):
        return self.select_file.text().strip()