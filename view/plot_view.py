from PyQt6.QtWidgets import QWidget, QVBoxLayout, QApplication
from PyQt6.QtCore import Qt
import pyqtgraph as pg
from pyqtgraph.exporters import ImageExporter


class PlotView(QWidget):
    """Render one or more measurement series with pyqtgraph."""

    def __init__(self, parent=None):
        # Initialize the embedded pyqtgraph widget and layout.
        super().__init__(parent)

        self.plot_widget = pg.PlotWidget()

        layout = QVBoxLayout()
        layout.addWidget(self.plot_widget)
        self.setLayout(layout)

        self.pen = pg.mkPen(color=(0, 0, 255), width=3)

    def set_plots(self, series_list, title="", label_x="", unit_x="", label_y="", unit_y=""):
        # Re-render complete chart state for the current selection.
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

    def export_file(self, plot_widget_dict, file_path, scale=3, transparent=False):
        """
        the plot with optional high resolution and transparent background.
        """
        plot_widget = plot_widget_dict.get("plot_widget")
        if plot_widget is None:
            raise ValueError("No plot widget provided")

        try:
            exporter = ImageExporter(plot_widget.plotItem)

            # original size
            orig_size = plot_widget.size()
            # Apply scale factor
            exporter.parameters()['width'] = orig_size.width() * scale
            exporter.parameters()['height'] = orig_size.height() * scale

            # Transparent background
            if transparent:
                exporter.parameters()['background'] = (0, 0, 0, 0)  # fully transparent

            exporter.export(file_path)
        except Exception as e:
            raise RuntimeError(f"Export failed: {e}") from e
