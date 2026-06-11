from pathlib import Path

class ImportController:

	def __init__(self, importers):
		if importers is None:
			raise ValueError("importers must be provided.")
		self.importers = importers

	def import_file(self, file_path):
		path = Path(file_path)

		for importer in self.importers:
			if importer.can_import(path):
				return importer.import_file(path)

		raise ValueError(f"No importer registered for file type: {path.suffix}")
