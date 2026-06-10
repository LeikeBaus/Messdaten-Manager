from pathlib import Path

from services.importers.csv_importer import CSVImporter
from services.importers.json_importer import JSONImporter


class ImportController:

	def __init__(self, importers):
		self.importers = importers or [CSVImporter(), JSONImporter()]

	def import_file(self, file_path):
		path = Path(file_path)

		for importer in self.importers:
			if importer.can_import(path):
				return importer.import_file(path)

		raise ValueError(f"No importer registered for file type: {path.suffix}")
