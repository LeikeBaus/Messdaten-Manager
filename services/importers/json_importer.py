import json
from pathlib import Path

from services.importers.importer import Importer

class JSONImporter(Importer):

    SUPPORTED_EXTENSIONS = ['json']

    def import_file(self, file_path):
        path = Path(file_path)

        with path.open("r", encoding="utf-8") as file_handle:
            data = json.load(file_handle)

        return data