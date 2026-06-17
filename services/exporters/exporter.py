from abc import ABC, abstractmethod
from pathlib import Path


class Exporter(ABC):
	"""Define the extension-based contract for export handlers."""

	SUPPORTED_EXTENSIONS = ()

	def can_export(self, file_path):
		# Match exporter responsibility by file extension.
		path = Path(file_path)
		suffix = path.suffix.lower().lstrip(".")

		if self.SUPPORTED_EXTENSIONS:
			return suffix in self.SUPPORTED_EXTENSIONS

		return False

	@abstractmethod
	def export_file(self, payload, file_path):
		# Subclasses must serialize payloads to the given path.
		raise NotImplementedError
