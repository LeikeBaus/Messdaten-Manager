import csv
from pathlib import Path

from services.exporters.exporter import Exporter


class CSVExporter(Exporter):
	"""Export tabular payloads to CSV files."""

	SUPPORTED_EXTENSIONS = ("csv")

	def export_file(self, payload, file_path):
		path = Path(file_path)
		path.parent.mkdir(parents=True, exist_ok=True)

		headers = list((payload or {}).get("headers") or [])
		rows = list((payload or {}).get("rows") or [])

		with path.open("w", encoding="utf-8", newline="") as file_handle:
			# The first row is treated as column headers.
			writer = csv.writer(file_handle)
			if headers:
				writer.writerow(headers)
			writer.writerows(rows)

		return path
