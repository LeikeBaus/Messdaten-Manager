import json
from pathlib import Path

from services.exporters.exporter import Exporter


class JSONExporter(Exporter):
	"""Export structured payloads to JSON files."""

	SUPPORTED_EXTENSIONS = ("json",)

	def export_file(self, payload, file_path):
		path = Path(file_path)
		path.parent.mkdir(parents=True, exist_ok=True)

		# Persist readable JSON to simplify manual inspection.
		with path.open("w", encoding="utf-8") as file_handle:
			json.dump(payload, file_handle, ensure_ascii=False, indent=2)

		return path
