from pathlib import Path
from datetime import datetime

from PyQt6.QtWidgets import QDialog, QMessageBox, QFileDialog

from model.experiment_data_classes import Experiment, MeasurementSeries, MeasurementData
from controller.experiment_persistence import ExperimentPersistence
from controller.selection_context import SelectionContext
from controller.experiment_view_updater import ExperimentViewUpdater
from services.importers.csv_importer import CSVImporter
from services.importers.json_importer import JSONImporter
from services.exporters.csv_exporter import CSVExporter
from services.exporters.json_exporter import JSONExporter
from services.exporters.plot_exporter import PlotExporter
from view.import_dialog import ImportDialog
from model.experiment_tree_model import ExperimentTreeModel, NODE_TYPE_EXPERIMENT, NODE_TYPE_MEASUREMENT
from model.measurement_table_model import MeasurementTableModel


class ExperimentController:
	"""Coordinate user actions between UI, repository, and persistence."""

	def __init__(self, main_window, repository):
		# Initialize controller dependencies and connect startup flow.
		self.main_window = main_window
		self.repository = repository
		# Import/export strategies are selected by file extension.
		self.importers = [CSVImporter(), JSONImporter()]
		self.exporters = [CSVExporter(), JSONExporter()]

		self.experiment_tree_model = ExperimentTreeModel()
		self.measurement_table_model = MeasurementTableModel()
		self.persistence = ExperimentPersistence(self.importers, self.exporters)
		self.plot_exporter = PlotExporter()

		self.main_window.set_experiment_tree_model(self.experiment_tree_model)
		self.main_window.set_measurement_model(self.measurement_table_model)
		self.selection_context = SelectionContext(self.main_window.experiment_tree_view, self.experiment_tree_model)
		self.view_updater = ExperimentViewUpdater(self.main_window, self.measurement_table_model)

		self._wire_actions()

		self._load_workspace_experiments()
		self.refresh_views()
		self._apply_selection_to_views()

	def _wire_actions(self):
		# Central action wiring keeps UI elements free of business logic.
		actions = self.main_window.actions
		actions.experiment_new.triggered.connect(self.create_experiment)
		actions.experiment_load.triggered.connect(self.load_experiment)
		actions.experiment_save.triggered.connect(self.save_experiment)
		actions.experiment_delete.triggered.connect(self.delete_experiments)

		actions.measurement_new.triggered.connect(self.create_measurement)
		actions.measurement_import.triggered.connect(self.import_measurement)
		actions.measurement_save.triggered.connect(self.save_measurement)
		actions.measurement_delete.triggered.connect(self.delete_measurements)

		actions.plot_export.triggered.connect(self.export_plot)

		selection_model = self.main_window.experiment_tree_view.tree_view.selectionModel()
		if selection_model is not None:
			selection_model.selectionChanged.connect(self._on_selection_changed)

	def _on_selection_changed(self, _selected, _deselected):
		# Refresh visible data whenever tree selection changes.
		self._apply_selection_to_views()

	def create_experiment(self):
		# Create a new empty experiment with default metadata.
		index = len(self.repository.list_experiments()) + 1
		experiment_id = f"experiment_{index}"
		timestamp = datetime.now().strftime("%Y-%m-%d")
		experiment = Experiment(
			id=experiment_id,
			metadata={
				"title": f"Neues Experiment {index}",
				"author": "",
				"date": timestamp,
				"description": "",
				"comment": "",
			},
			measurements=[],
		)
		self._upsert_and_refresh(experiment)

	def load_experiment(self):
		# Import an experiment from a selected file path.
		file_path = self._pick_import_file_path()
		if not file_path:
			return

		experiment = self.persistence.import_experiment_from_path(file_path)
		if experiment is None:
			self._show_error("Experiment laden", "Die ausgewaehlte Datei konnte nicht als Experiment geladen werden.")
			return

		self.repository.upsert(experiment)
		self.repository.set_current(experiment.id)
		self._refresh_selection_views()

	def save_experiment(self):
		# Persist the selected experiment and all contained measurements.
		experiment = self._require_selected_experiment("Experiment speichern")
		if experiment is None:
			return

		self.persistence.persist_experiment(experiment)
		self._show_info("Experiment speichern", f"Experiment '{experiment.id}' wurde gespeichert.")

	def delete_experiments(self):
		# Delete the currently selected experiment from the repository.
		experiment = self._require_selected_experiment("Experiment loeschen")
		if experiment is None:
			return

		self.repository.remove_experiments([experiment.id])
		self._refresh_selection_views()

	def create_measurement(self):
		# Append a new empty measurement to the selected experiment.
		experiment = self._require_selected_experiment("Neue Messreihe")
		if experiment is None:
			return

		experiment.measurements.append(self._new_measurement(experiment))
		self._upsert_and_refresh(experiment)

	def import_measurement(self):
		# Import a measurement file and attach it to the selected experiment.
		experiment = self._require_selected_experiment("Messreihe importieren")
		if experiment is None:
			return

		file_path = self._pick_import_file_path()
		if not file_path:
			return

		payload = self.persistence.import_file(file_path)
		if not isinstance(payload, dict):
			self._show_error("Messreihe importieren", "Datei konnte nicht importiert werden.")
			return

		experiment.measurements.append(
			self._new_measurement(
				experiment,
				name=Path(file_path).stem,
				headers=payload.get("headers") or [],
				rows=payload.get("rows") or [],
			)
		)
		self._upsert_and_refresh(experiment)

	def save_measurement(self):
		# Persist only the selected measurement and update metadata file.
		selection = self._require_selected_measurement("Messreihe speichern")
		if selection is None:
			return

		experiment, measurement = selection

		experiment_dir = self.persistence.experiment_dir(experiment.id)
		experiment_dir.mkdir(parents=True, exist_ok=True)
		self.persistence.write_measurement_csv(experiment_dir, measurement)
		self.persistence.write_experiment_metadata(experiment)

		self._show_info("Messreihe speichern", "1 Messreihe gespeichert.")

	def delete_measurements(self):
		# Remove the selected measurement from its parent experiment.
		selection = self._require_selected_measurement("Messreihe loeschen")
		if selection is None:
			return

		experiment, measurement = selection

		experiment.measurements = [
			entry for entry in experiment.measurements
			if entry.id != measurement.id
		]
		self._upsert_and_refresh(experiment)

	def export_plot(self):
		# Export the currently visible plot into an image file.
		transparent = self.main_window.plot_view.transparent_cb.isChecked()
		file_path, _ = QFileDialog.getSaveFileName(
			self.main_window,
			"Plot exportieren",
			"",
			"PNG (*.png);;JPEG (*.jpg *.jpeg)"
		)
		if not file_path:
			return
		QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
		try:
			self.plot_exporter.export_file(
				{"plot_widget": self.main_window.plot_view.plot_widget},
				file_path,
				scale=3,                # high resolution
            	transparent=transparent
			)
		except Exception as exc:
			QApplication.restoreOverrideCursor()
        	self._show_error("Plot exportieren", f"Plot konnte nicht exportiert werden: {exc}")
        	return
    	finally:
        	QApplication.restoreOverrideCursor()

	def copy_plot_to_clipboard(self):
    	self.main_window.plot_view.copy_to_clipboard()

	def refresh_views(self):
		# Rebuild the tree view from the repository snapshot.
		experiments = self.repository.list_experiments()
		self.experiment_tree_model.set_experiments(experiments)
		self.main_window.experiment_tree_view.tree_view.expandAll()

	def _apply_selection_to_views(self):
		# Translate current tree selection to concrete view updates.
		selected = self.selection_context.selected_node_info()

		if selected is None:
			self.view_updater.clear()
			return

		experiment = self.repository.get(selected["experiment_id"])

		if selected["type"] == NODE_TYPE_EXPERIMENT:
			self.view_updater.show_experiment(experiment)
			return

		if selected["type"] == NODE_TYPE_MEASUREMENT:
			measurement = self._find_measurement(experiment, selected["measurement_id"]) if experiment is not None else None
			self.view_updater.show_measurement(experiment, measurement)
			return

		self.view_updater.clear()

	def _require_selected_experiment(self, action_name):
		# Return selected experiment or show a user-facing error.
		experiment_id = self.selection_context.selected_experiment_id()
		if experiment_id is None:
			self._show_error(action_name, "Bitte waehlen Sie ein Experiment aus.")
			return None

		experiment = self.repository.get(experiment_id)
		if experiment is None:
			self._show_error(action_name, "Experiment konnte nicht gefunden werden.")
			return None

		return experiment

	def _show_error(self, title, text):
		# Show a warning dialog with an operation-specific message.
		QMessageBox.warning(self.main_window, title, text)

	def _show_info(self, title, text):
		# Show an informational dialog after successful operations.
		QMessageBox.information(self.main_window, title, text)

	def _find_measurement(self, experiment, measurement_id):
		# Locate a measurement by id in a given experiment.
		return next((measurement for measurement in experiment.measurements if measurement.id == measurement_id), None)

	def _pick_import_file_path(self):
		# Open the import dialog and return the selected file path.
		dialog = ImportDialog(self.main_window)
		if dialog.exec() != QDialog.DialogCode.Accepted:
			return None
		return dialog.selected_file_path()

	def _refresh_selection_views(self):
		# Sync tree, metadata, table, and plot after data changes.
		self.refresh_views()
		self._apply_selection_to_views()

	def _upsert_and_refresh(self, experiment):
		# Upsert experiment in repository and refresh visible UI.
		self.repository.upsert(experiment)
		self._refresh_selection_views()

	def _new_measurement(self, experiment, name=None, headers=None, rows=None):
		# Build a measurement object with sensible default axis/plot settings.
		headers = headers or ["x", "y"]
		rows = rows or []
		index = len(experiment.measurements) + 1
		return MeasurementSeries(
			id=f"{experiment.id}_measurement_{index}",
			name=name or f"Messreihe {index}",
			data=MeasurementData(headers=headers, rows=rows),
			x={"title": headers[0] if len(headers) > 0 else "X", "type": "float", "unit": ""},
			y={"title": headers[1] if len(headers) > 1 else "Y", "type": "float", "unit": ""},
			plot={"visible": True, "color": "#1f77b4", "line_width": 2},
		)

	def _require_selected_measurement(self, action_name):
		# Return selected experiment/measurement pair or show an error.
		measurement_ref = self.selection_context.selected_measurement_ref()
		if measurement_ref is None:
			self._show_error(action_name, "Bitte waehlen Sie mindestens eine Messreihe aus.")
			return None

		experiment = self.repository.get(measurement_ref["experiment_id"])
		if experiment is None:
			self._show_error(action_name, "Experiment oder Messreihe konnte nicht gefunden werden.")
			return None

		measurement = self._find_measurement(experiment, measurement_ref["measurement_id"])
		if measurement is None:
			self._show_error(action_name, "Experiment oder Messreihe konnte nicht gefunden werden.")
			return None

		return experiment, measurement

	def _load_workspace_experiments(self):
		# Load persisted workspace experiments during startup.
		for experiment in self.persistence.load_workspace_experiments():
			if experiment is not None:
				self.repository.upsert(experiment)
