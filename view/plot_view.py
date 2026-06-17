from PyQt6.QtWidgets import QWidget, QVBoxLayout
from services.exporters.plot_exporter import PlotExporter
import tempfile
import os
import pyqtgraph as pg


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
     def copy_to_clipboard(self):
        """Plot as PNG to clipboard."""
        exporter = PlotExporter()
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
            temp_path = tmp.name

        try:
            transparent = self.transparent_cb.isChecked()
            exporter.export_file(
                {"plot_widget": self.plot_widget},
                temp_path,
                scale=2,          # moderate resolution for clipboard
                transparent=transparent
            )
            pixmap = QPixmap(temp_path)
            QGuiApplication.clipboard().setPixmap(pixmap)
            QMessageBox.information(self, "Copied", "Plot copied to clipboard as image.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to copy: {e}")
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)
