from abc import ABC, abstractmethod
from pathlib import Path


class Importer(ABC):
	"""Define the extension-based contract for import handlers."""

	SUPPORTED_EXTENSIONS = ()

	def can_import(self, file_path):
		"""Return True when this importer can handle the given file."""
		# Compare normalized file suffix against supported extensions.
		path = Path(file_path)
		suffix = path.suffix.lower().lstrip(".")

		if self.SUPPORTED_EXTENSIONS:
			return suffix in self.SUPPORTED_EXTENSIONS

		return False

	@abstractmethod
	def import_file(self, file_path):
		"""Import the file at *file_path* and return experiment data."""
		# Subclasses must parse and return a normalized payload.
		raise NotImplementedError
