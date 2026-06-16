from pathlib import Path

from model.experiment import Experiment, MeasurementSeries
from model.measurement_data import MeasurementData


class ExperimentPersistence:
    def __init__(self, importers):
        self.importers = list(importers)

    def load_workspace_experiments(self):
        experiments = []
        root_path = (Path("data") / "experiments")

        for experiment_dir in sorted(root_path.iterdir()):
            if not experiment_dir.is_dir():
                continue

            metadata_file = experiment_dir / "metadata.json"
            if not metadata_file.exists():
                continue

            experiment = self.load_experiment_from_metadata_file(metadata_file)
            if experiment is not None:
                experiments.append(experiment)

        return experiments

    def import_file(self, file_path):
        for importer in self.importers:
            if importer.can_import(file_path):
                return importer.import_file(file_path)
        return None

    def import_experiment_from_path(self, file_path):
        path = Path(file_path)

        if path.name == "metadata.json":
            return self.load_experiment_from_metadata_file(path)

        return self.build_experiment_from_import(self.import_file(file_path), file_path)

    def load_experiment_from_metadata_file(self, metadata_file_path):
        path = Path(metadata_file_path)

        metadata_doc = self.import_file(str(path)) or {}
        if not isinstance(metadata_doc, dict):
            metadata_doc = {}

        experiment_info = metadata_doc.get("experiment", {})
        experiment_id = experiment_info.get("id") or path.parent.name

        experiment_metadata = {
            "title": experiment_info.get("title", experiment_id),
            "author": experiment_info.get("author", ""),
            "date": experiment_info.get("date", ""),
            "description": experiment_info.get("description", ""),
            "comment": experiment_info.get("comment", ""),
        }

        measurements = []
        for measurement_def in metadata_doc.get("measurements", []):
            measurement_file = path.parent / measurement_def.get("file", "")
            if not measurement_file.exists():
                continue

            measurement_payload = self.import_file(str(measurement_file)) or {}
            if not isinstance(measurement_payload, dict):
                measurement_payload = {}

            measurement_data = MeasurementData(
                headers=measurement_payload.get("headers") or [],
                rows=measurement_payload.get("rows") or [],
            )

            measurement = MeasurementSeries(
                id=measurement_def.get("id") or measurement_file.stem,
                name=measurement_def.get("name") or measurement_file.stem,
                data=measurement_data,
                x=measurement_def.get("x") or {},
                y=measurement_def.get("y") or {},
                plot=measurement_def.get("plot") or {},
            )
            measurements.append(measurement)

        return Experiment(id=experiment_id, metadata=experiment_metadata, measurements=measurements)

    def build_experiment_from_import(self, imported_data, file_path):
        if not isinstance(imported_data, dict):
            return None

        experiment_id = imported_data.get("id") or Path(file_path).stem
        metadata = imported_data.get("metadata") or {"title": experiment_id}
        measurement = self._measurement_from_payload(experiment_id, imported_data)
        return Experiment(id=experiment_id, metadata=metadata, measurements=[measurement])

    def _measurement_from_payload(self, experiment_id, payload):
        headers = payload.get("headers") or []
        rows = payload.get("rows") or []
        return MeasurementSeries(
            id=f"{experiment_id}_measurement_1",
            name="Messung 1",
            data=MeasurementData(headers=headers, rows=rows),
            x={"title": headers[0] if len(headers) > 0 else "X", "type": "float", "unit": ""},
            y={"title": headers[1] if len(headers) > 1 else "Y", "type": "float", "unit": ""},
            plot={"visible": True, "color": "#1f77b4", "line_width": 2},
        )
    
    def measurement_file_name(self, measurement):
        safe_id = measurement.id.replace(" ", "_")
        return f"{safe_id}.csv"
    
    def experiment_dir(self, experiment_id):
        return Path("data") / "experiments" / experiment_id

    def persist_experiment(self, experiment):
        pass

    def write_measurement_csv(self, experiment_dir, measurement):
        pass

    def write_experiment_metadata(self, experiment):
        pass
