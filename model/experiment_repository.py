import csv
import json
import shutil
from pathlib import Path


class ExperimentRepository:
	"""
	Persistence layer for experiments stored in folders.
	"""

	METADATA_FILE = "metadata.json"
	DATA_FILE = "data.csv"

	def __init__(self, data_dir):
		self.data_dir = Path(data_dir)
		self.data_dir.mkdir(parents=True, exist_ok=True)

	def list_experiments(self):
		"""Return available experiment folders."""
		experiments = []
		
		for folder in self.data_dir.iterdir():
			if not folder.is_dir():
				continue

			metadata_path = folder / self.METADATA_FILE
			csv_path = folder / self.DATA_FILE
			metadata_title = None

			if metadata_path.exists():
				try:
					metadata = self._read_metadata(metadata_path)
					metadata_title = (
						metadata.get("info", {}).get("laboratory_title", "Untitled Experiment")
					)
				except (json.JSONDecodeError, OSError):
					metadata_title = None

			experiments.append(
				{
					"id": folder.name,
					"path": str(folder),
					"has_metadata": metadata_path.exists(),
					"has_data_csv": csv_path.exists(),
					"title": metadata_title,
				}
			)

		return experiments

	def exists(self, experiment_id):
		"""Check if an experiment with the given ID exists."""
		return self._experiment_dir(experiment_id).is_dir()

	def load(self, experiment_id):
		"""Load one experiment from canonical storage format."""
		experiment_dir = self._experiment_dir(experiment_id)

		metadata_path = experiment_dir / self.METADATA_FILE
		csv_path = experiment_dir / self.DATA_FILE

		metadata = self._read_metadata(metadata_path)
		headers, rows = self._read_csv(csv_path)

		return {
			"id": experiment_id,
			"metadata": metadata,
			"headers": headers,
			"rows": rows,
		}

	def save(self, experiment_id, metadata, headers, rows):
		"""Save one experiment using metadata.json + data.csv files."""
		experiment_dir = self._experiment_dir(experiment_id)

		experiment_dir.mkdir(parents=True, exist_ok=True)
		metadata_path = experiment_dir / self.METADATA_FILE
		csv_path = experiment_dir / self.DATA_FILE
		
		self._write_metadata(metadata_path, metadata)
		self._write_csv(csv_path, headers, rows)

	def delete(self, experiment_id):
		experiment_dir = self._experiment_dir(experiment_id)
		shutil.rmtree(experiment_dir)

	def _experiment_dir(self, experiment_id):
		experiment_id = experiment_id.strip()
		return self.data_dir / experiment_id

	@staticmethod
	def _read_metadata(path):
		with path.open("r", encoding="utf-8") as f:
			data = json.load(f)
		return data

	@staticmethod
	def _write_metadata(path, metadata):
		with path.open("w", encoding="utf-8") as f:
			json.dump(metadata, f, indent=2)

	@staticmethod
	def _read_csv(path):
		with path.open("r", encoding="utf-8", newline="") as f:
			reader = csv.reader(f, skipinitialspace=True)
			all_rows = [row for row in reader if row]

		headers = all_rows[0]
		rows = all_rows[1:]
		return headers, rows

	@staticmethod
	def _write_csv(path, headers, rows):
		with path.open("w", encoding="utf-8", newline="") as f:
			writer = csv.writer(f)
			if headers:
				writer.writerow(headers)
			for row in rows:
				writer.writerow(row)
