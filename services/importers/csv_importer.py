import csv
from pathlib import Path

from services.importers.importer import Importer


class CSVImporter(Importer):

	SUPPORTED_EXTENSIONS = ("csv",)

	def import_file(self, file_path):
		path = Path(file_path)

		with path.open("r", encoding="utf-8", newline="") as file_handle:
			reader = csv.reader(file_handle, skipinitialspace=True)
			rows = [row for row in reader if any(cell.strip() for cell in row)]

		if not rows:
			raise ValueError(f"CSV file is empty: {path}")

		headers = [cell.strip() for cell in rows[0]]
		data_rows = [[cell.strip() for cell in row] for row in rows[1:]]

		return {
			"id": path.stem,
			"metadata": {},
			"headers": headers,
			"rows": data_rows,
		}
