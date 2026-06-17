import json
from pathlib import Path

from services.importers.importer import Importer

class JSONImporter(Importer):
    """Import measurement or metadata payloads from JSON files."""

    SUPPORTED_EXTENSIONS = ("json")

    def import_file(self, file_path):
        # Parse JSON and return raw object structure.
        path = Path(file_path)

        # JSON payloads are passed through as-is for flexible schemas.
        with path.open("r", encoding="utf-8") as file_handle:
            data = json.load(file_handle)

        return data