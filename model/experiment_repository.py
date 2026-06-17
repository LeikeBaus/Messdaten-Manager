from model.experiment_data_classes import Experiment


class ExperimentRepository:
	"""Manage experiments in memory and track the current selection id."""

	def __init__(self):
		# Initialize empty repository state.
		self._experiments = []
		self._current_experiment_id = None

	def upsert(self, experiment: Experiment):
		# Replace by id or append when it is a new experiment.
		for index, existing in enumerate(self._experiments):
			if existing.id == experiment.id:
				self._experiments[index] = experiment
				return

		self._experiments.append(experiment)

	def list_experiments(self):
		# Return a copy to protect internal repository state.
		return list(self._experiments)

	def get(self, experiment_id):
		# Look up an experiment by its id.
		for experiment in self._experiments:
			if experiment.id == experiment_id:
				return experiment
		return None

	def set_current(self, experiment_id):
		# Update current experiment only if the id exists.
		if self.get(experiment_id) is not None:
			self._current_experiment_id = experiment_id

	def get_current(self):
		# Return current experiment or first available fallback.
		if self._current_experiment_id is None and self._experiments:
			return self._experiments[0]
		if self._current_experiment_id is None:
			return None
		return self.get(self._current_experiment_id)

	def remove_experiments(self, experiment_ids):
		# Keep current selection valid after bulk deletion.
		ids = set(experiment_ids)
		self._experiments = [experiment for experiment in self._experiments if experiment.id not in ids]

		if self._current_experiment_id in ids:
			self._current_experiment_id = self._experiments[0].id if self._experiments else None
