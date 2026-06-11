from PyQt6.QtWidgets import QWidget, QLabel, QLineEdit, QTextEdit, QGridLayout

class MetaWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setMaximumHeight(150)

        self.titel_label = QLabel("Titel:")
        self.titel = QLineEdit()

        self.date_label = QLabel("Datum:")
        self.date = QLineEdit()

        self.author_label = QLabel("Autor/-in:")
        self.author = QLineEdit()

        self.description_label = QLabel("Beschreibung:")
        self.description = QTextEdit()

        self.comment_label = QLabel("Kommentar:")
        self.comment = QTextEdit()

        grid = QGridLayout()
        grid.addWidget(self.titel_label, 0, 0)
        grid.addWidget(self.date_label, 1, 0)
        grid.addWidget(self.author_label, 2, 0)

        grid.addWidget(self.titel, 0, 1)
        grid.addWidget(self.date, 1, 1)
        grid.addWidget(self.author, 2, 1)

        grid.addWidget(self.description_label, 0, 2)
        grid.addWidget(self.description, 1, 2, 2, 1)

        grid.addWidget(self.comment_label, 0, 3)
        grid.addWidget(self.comment, 1, 3, 2, 1)
        grid.setSpacing(20)

        self.setLayout(grid)


    def set_meta(self, titel="", author="", date="", description="", comment=""):
        self.titel.setText(titel)
        self.author.setText(author)
        self.date.setText(date)
        self.description.setPlainText(description)
        self.comment.setPlainText(comment)