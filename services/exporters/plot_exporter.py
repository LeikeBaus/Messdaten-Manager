from pathlib import Path

from pyqtgraph.exporters import ImageExporter

from services.exporters.exporter import Exporter


class PlotExporter(Exporter):
	"""Export the rendered plot widget as an image file."""

	SUPPORTED_EXTENSIONS = ("png", "jpg", "jpeg")

	def export_file(self, payload, file_path):
		path = Path(file_path)
		path.parent.mkdir(parents=True, exist_ok=True)

		plot_widget = (payload or {}).get("plot_widget")
		if plot_widget is None:
			raise ValueError("Missing plot_widget payload for plot export")

		# Export the currently rendered plot item as an image.
		exporter = ImageExporter(plot_widget.plotItem)
		exporter.export(str(path))
		return path
	def export_plot(self):
    # Transparent setting from plot view
    transparent = self.main_window.plot_view.transparent_cb.isChecked()

    file_path, _ = QFileDialog.getSaveFileName(
        self.main_window,
        "Plot exportieren",
        "",
        "PNG (*.png);;JPEG (*.jpg *.jpeg)"
    )
    if not file_path:
        return

    # Cursor
    QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
    try:
        self.plot_exporter.export_file(
            {"plot_widget": self.main_window.plot_view.plot_widget},
            file_path,
            scale=3,                # high resolution
            transparent=transparent
        )
    except Exception as exc:
        QApplication.restoreOverrideCursor()
        self._show_error("Plot exportieren", f"Plot konnte nicht exportiert werden: {exc}")
        return
    finally:
        QApplication.restoreOverrideCursor()

    self._show_info("Plot exportieren", "Plot erfolgreich exportiert.")
