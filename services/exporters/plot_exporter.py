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
