from model.experiment import Experiment


class ExperimentRepository:
	def __init__(self):
		self._experiments = []
		self._current_experiment_id = None

	def upsert(self, experiment: Experiment):
		for index, existing in enumerate(self._experiments):
			if existing.id == experiment.id:
				self._experiments[index] = experiment
				return

		self._experiments.append(experiment)

	def list_experiments(self):
		return list(self._experiments)

	def get(self, experiment_id):
		for experiment in self._experiments:
			if experiment.id == experiment_id:
				return experiment
		return None

	def set_current(self, experiment_id):
		if self.get(experiment_id) is not None:
			self._current_experiment_id = experiment_id

	def get_current(self):
		if self._current_experiment_id is None and self._experiments:
			return self._experiments[0]
		if self._current_experiment_id is None:
			return None
		return self.get(self._current_experiment_id)

	def remove_experiments(self, experiment_ids):
		ids = set(experiment_ids)
		self._experiments = [experiment for experiment in self._experiments if experiment.id not in ids]

		if self._current_experiment_id in ids:
			self._current_experiment_id = self._experiments[0].id if self._experiments else None
