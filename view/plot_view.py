from PyQt6.QtWidgets import QWidget, QVBoxLayout
import pyqtgraph as pg


class PlotView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.plot_widget = pg.PlotWidget()

        layout = QVBoxLayout()
        layout.addWidget(self.plot_widget)
        self.setLayout(layout)

        self.pen = pg.mkPen(color=(0, 0, 255), width=3)

    def set_plots(self, series_list, title="", label_x="", unit_x="", label_y="", unit_y=""):
        self.plot_widget.clear()
        self.plot_widget.setTitle(title, size="16pt")

        if unit_x:
            self.plot_widget.setLabel("bottom", f"{label_x} in {unit_x}")
        else:
            self.plot_widget.setLabel("bottom", label_x)

        if unit_y:
            self.plot_widget.setLabel("left", f"{label_y} in {unit_y}")
        else:
            self.plot_widget.setLabel("left", label_y)

        if not series_list:
            return

        self.plot_widget.addLegend()
        for series in series_list:
            color = series.get("color", "#1f77b4")
            width = int(series.get("line_width", 2))
            pen = pg.mkPen(color=color, width=width)
            self.plot_widget.plot(
                series.get("x", []),
                series.get("y", []),
                pen=pen,
                name=series.get("name", "Messreihe"),
            )
