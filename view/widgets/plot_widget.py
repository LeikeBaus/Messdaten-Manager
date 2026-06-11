from PyQt6.QtWidgets import QWidget, QVBoxLayout
import pyqtgraph as pg


class PlotWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.plot_widget = pg.PlotWidget()

        layout = QVBoxLayout()
        layout.addWidget(self.plot_widget)
        self.setLayout(layout)

        # Linie
        self.pen = pg.mkPen(color=(0, 0, 255), width=5)

    def set_plot(self, data_x, data_y, title="", label_x="", unit_x="", label_y="", unit_y=""):
        self.plot_widget.clear()
        # Titel
        self.plot_widget.setTitle(title, size="16pt")

        # Achsenbeschriftung
        if unit_x == "":
            self.plot_widget.setLabel('bottom', label_x)
        else:
            self.plot_widget.setLabel('bottom', label_x + " in " + unit_x)

        if unit_y == "":
            self.plot_widget.setLabel('left', label_y)
        else:
            self.plot_widget.setLabel('left', label_y + " in " + unit_y)

        self.plot_widget.plot(data_x, data_y, pen=self.pen)



