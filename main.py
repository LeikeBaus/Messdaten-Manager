import sys
from PyQt6.QtWidgets import QApplication, QMainWindow
from view.plot_view import PlotView


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Messdaten-Manager")
        self.setGeometry(100, 100, 800, 600)
        # Erstellt man einen Window

        self.plot_view = PlotView(self)
        self.setCentralWidget(self.plot_view)
        # Erstellt man eine mittlere Plot View

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())