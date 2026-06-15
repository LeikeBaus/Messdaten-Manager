from pathlib import Path
import csv

from model.experiment import Experiment
from model.measurement_data import MeasurementData
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
        data_rows = rows[1:]

        # Transponieren: Spalten werden zu MeasurementData-Objekten
        experiment = Experiment(
            experiment_id=path.stem,
            name=path.stem,
        )

        for col_idx, header in enumerate(headers):
            try:
                # Werte aus dieser Spalte extrahieren und zu float konvertieren
                col_values = [
                    float(row[col_idx].strip().replace(",", "."))
                    for row in data_rows
                    if col_idx < len(row)
                ]
                
                measurement = MeasurementData(
                    name=header,
                    unit="",
                    values=col_values
                )
                experiment.add_measurement(measurement)
            
            except (ValueError, IndexError) as e:
                raise ValueError(
                    f"Cannot convert column '{header}' to numeric values: {e}"
                )

        return experiment