from experiment_persistence import ExperimentPersistence
from services.importers.csv_importer import CSVImporter
from services.importers.json_importer import JSONImporter

class ExperimentController:
	def __init__(self, main_window, repository):
		self.main_window = main_window
		self.repository = repository
		self.importers = [CSVImporter(), JSONImporter()]
		self.persistence = ExperimentPersistence(self.importers)
		
	def _load_workspace_experiments(self):
		for experiment in self.persistence.load_workspace_experiments():
			if experiment is not None:
				self.repository.upsert(experiment)