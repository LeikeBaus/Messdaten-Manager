from abc import ABC, abstractmethod
from pathlib import Path

class Importer(ABC):

	SUPPORTED_EXTENSIONS = ()

	def can_import(self, file_path):
		"""Return True when this importer can handle the given file."""
		path = Path(file_path)
		suffix = path.suffix.lower().lstrip(".")

		if self.SUPPORTED_EXTENSIONS:
			return suffix in self.SUPPORTED_EXTENSIONS

		return False

	@abstractmethod
	def import_file(self, file_path):
		"""Import the file at *file_path* and return experiment data."""
		raise NotImplementedError
