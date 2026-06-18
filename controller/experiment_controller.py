from pathlib import Path
from datetime import datetime

from PyQt6.QtWidgets import QDialog, QMessageBox, QFileDialog

from model.experiment_data_classes import Experiment, MeasurementSeries, MeasurementData
from model.experiment_tree_model import ExperimentTreeModel
from model.measurement_table_model import MeasurementTableModel
from services.importers.csv_importer import CSVImporter
from services.importers.json_importer import JSONImporter
from services.exporters.csv_exporter import CSVExporter
from services.exporters.json_exporter import JSONExporter
from services.exporters.plot_exporter import PlotExporter
from view.import_dialog import ImportDialog


class ExperimentController:

	def __init__(self, main_window, repository):
		self.main_window = main_window
		self.repository = repository
		self.importers = [CSVImporter(), JSONImporter()]
		self.exporters = [CSVExporter(), JSONExporter()]
		self.tree_model = ExperimentTreeModel()
		self.table_model = MeasurementTableModel()
		self.plot_exporter = PlotExporter()

		# Set models
		main_window.set_experiment_tree_model(self.tree_model)
		main_window.set_measurement_model(self.table_model)

		# Connect actions and selection changes.
		acts = main_window.actions
		acts.experiment_new.triggered.connect(self.create_experiment)
		acts.experiment_load.triggered.connect(self.load_experiment)
		acts.experiment_save.triggered.connect(self.save_experiment)
		acts.experiment_delete.triggered.connect(self.delete_experiments)
		acts.measurement_new.triggered.connect(self.create_measurement)
		acts.measurement_import.triggered.connect(self.import_measurement)
		acts.measurement_save.triggered.connect(self.save_measurement)
		acts.measurement_delete.triggered.connect(self.delete_measurements)
		acts.plot_export.triggered.connect(self.export_plot)
		main_window.experiment_tree_view.tree_view.selectionModel().selectionChanged.connect(self._on_selection)

		# Load existing experiments from the workspace.
		for exp in self._load_workspace():
			self.repository.upsert(exp)
		self._refresh()

	# --- Actions ---

	def create_experiment(self):
		idx = len(self.repository.list_experiments()) + 1
		self._upsert(Experiment(
			id=f"experiment_{idx}",
			metadata={"title": f"Neues Experiment {idx}", "author": "", "date": datetime.now().strftime("%Y-%m-%d"), "description": "", "comment": ""},
			measurements=[],
		))

	def load_experiment(self):
		path = self._pick_file()
		if not path:
			return
		exp = self._import_experiment(path)
		if exp is None:
			QMessageBox.warning(self.main_window, "Experiment laden", "Datei konnte nicht geladen werden.")
			return
		self.repository.upsert(exp)
		self.repository.set_current(exp.id)
		self._refresh()

	def save_experiment(self):
		exp = self._require_experiment("Experiment speichern")
		if exp:
			self._persist_experiment(exp)
			QMessageBox.information(self.main_window, "Experiment speichern", f"'{exp.id}' gespeichert.")

	def delete_experiments(self):
		exp = self._require_experiment("Experiment loeschen")
		if exp:
			self.repository.remove_experiments([exp.id])
			self._refresh()

	def create_measurement(self):
		exp = self._require_experiment("Neue Messreihe")
		if exp:
			exp.measurements.append(self._new_measurement(exp))
			self._upsert(exp)

	def import_measurement(self):
		exp = self._require_experiment("Messreihe importieren")
		if exp is None:
			return
		path = self._pick_file()
		if not path:
			return
		payload = self._import_file(path)
		if not isinstance(payload, dict):
			QMessageBox.warning(self.main_window, "Messreihe importieren", "Datei konnte nicht importiert werden.")
			return
		exp.measurements.append(self._new_measurement(exp, name=Path(path).stem, headers=payload.get("headers") or [], rows=payload.get("rows") or []))
		self._upsert(exp)

	def save_measurement(self):
		sel = self._require_measurement("Messreihe speichern")
		if sel:
			exp, meas = sel
			d = self._exp_dir(exp.id)
			d.mkdir(parents=True, exist_ok=True)
			self._write_csv(d, meas)
			self._write_metadata(exp)
			QMessageBox.information(self.main_window, "Messreihe speichern", "Messreihe gespeichert.")

	def delete_measurements(self):
		sel = self._require_measurement("Messreihe loeschen")
		if sel:
			exp, meas = sel
			exp.measurements = [m for m in exp.measurements if m.id != meas.id]
			self._upsert(exp)

	def export_plot(self):
		path, _ = QFileDialog.getSaveFileName(self.main_window, "Plot exportieren", "", "PNG (*.png);;JPEG (*.jpg *.jpeg)")
		if not path:
			return
		try:
			self.plot_exporter.export_file({"plot_widget": self.main_window.plot_view.plot_widget}, path)
		except Exception as exc:
			QMessageBox.warning(self.main_window, "Plot exportieren", f"Fehler: {exc}")
			return
		QMessageBox.information(self.main_window, "Plot exportieren", "Plot exportiert.")

	# --- View ---

	def _refresh(self):
		self.tree_model.set_experiments(self.repository.list_experiments())
		self.main_window.experiment_tree_view.tree_view.expandAll()
		self._on_selection()

	def _on_selection(self):
		info = self._selected_info()
		if info is None:
			self._clear_views()
			return
		exp = self.repository.get(info["experiment_id"])
		if info["type"] == "experiment":
			self._show_experiment(exp)
		elif info["type"] == "measurement":
			meas = next((m for m in exp.measurements if m.id == info["measurement_id"]), None) if exp else None
			self._show_measurement(exp, meas)
		else:
			self._clear_views()

	def _clear_views(self):
		self.table_model.set_measurements([], [])
		self.main_window.set_meta({})
		self.main_window.set_plots([], title="", label_x="", label_y="")

	def _show_experiment(self, exp):
		if exp is None:
			self._clear_views()
			return
		first = exp.measurements[0] if exp.measurements else None
		self.table_model.set_measurements(first.data.headers if first else [], first.data.rows if first else [])
		self.main_window.set_meta(exp.metadata)
		series = []
		for m in exp.measurements:
			x, y = m.data.numeric_xy_series()
			if x and y:
				series.append(self._to_series(m, x, y))
		self.main_window.set_plots(
			series,
			title=exp.metadata.get("title", exp.id),
			label_x=first.x.get("title", "X") if first else "X",
			label_y=first.y.get("title", "Y") if first else "Y",
			unit_x=first.x.get("unit", "") if first else "",
			unit_y=first.y.get("unit", "") if first else "",
		)

	def _show_measurement(self, exp, meas):
		if exp is None or meas is None:
			self._clear_views()
			return
		self.table_model.set_measurements(meas.data.headers, meas.data.rows)
		self.main_window.set_meta(exp.metadata)
		self.main_window.set_plots(
			[self._to_series(meas)],
			title=exp.metadata.get("title", exp.id),
			label_x=meas.x.get("title", "X"), label_y=meas.y.get("title", "Y"),
			unit_x=meas.x.get("unit", ""), unit_y=meas.y.get("unit", ""),
		)

	def _to_series(self, measurement, x=None, y=None):
		if x is None or y is None:
			x, y = measurement.data.numeric_xy_series()
		return {"name": measurement.name, "x": x, "y": y, "color": measurement.plot.get("color", "#1f77b4"), "line_width": measurement.plot.get("line_width", 2)}

	# --- Selection helpers ---

	def _selected_info(self):
		index = self.main_window.experiment_tree_view.selected_index()
		return self.tree_model.item_info(index) if index is not None else None

	def _require_experiment(self, action):
		info = self._selected_info()
		if info is None or info["type"] != "experiment":
			QMessageBox.warning(self.main_window, action, "Bitte waehlen Sie ein Experiment aus.")
			return None
		exp = self.repository.get(info["experiment_id"])
		if exp is None:
			QMessageBox.warning(self.main_window, action, "Experiment nicht gefunden.")
			return None
		return exp

	def _require_measurement(self, action):
		info = self._selected_info()
		if info is None or info["type"] != "measurement":
			QMessageBox.warning(self.main_window, action, "Bitte waehlen Sie eine Messreihe aus.")
			return None
		exp = self.repository.get(info["experiment_id"])
		meas = next((m for m in exp.measurements if m.id == info["measurement_id"]), None) if exp else None
		if exp is None or meas is None:
			QMessageBox.warning(self.main_window, action, "Messreihe nicht gefunden.")
			return None
		return exp, meas

	def _upsert(self, exp):
		self.repository.upsert(exp)
		self._refresh()

	# --- Persistence ---

	def _load_workspace(self):
		root = Path("data") / "experiments"
		experiments = []
		for d in sorted(root.iterdir()):
			if d.is_dir() and (d / "metadata.json").exists():
				exp = self._import_experiment(str(d / "metadata.json"))
				if exp:
					experiments.append(exp)
		return experiments

	def _import_file(self, path):
		for imp in self.importers:
			if imp.can_import(path):
				return imp.import_file(path)
		return None

	def _import_experiment(self, file_path):
		path = Path(file_path)
		if path.name == "metadata.json":
			return self._load_from_metadata(path)
		data = self._import_file(file_path)
		if not isinstance(data, dict):
			return None
		exp_id = data.get("id") or path.stem
		return Experiment(id=exp_id, metadata=data.get("metadata") or {"title": exp_id}, measurements=[self._payload_to_measurement(exp_id, data)])

	def _load_from_metadata(self, meta_path):
		doc = self._import_file(str(meta_path)) or {}
		if not isinstance(doc, dict):
			doc = {}
		info = doc.get("experiment", {})
		exp_id = info.get("id") or meta_path.parent.name
		metadata = {"title": info.get("title", exp_id), **{k: info.get(k, "") for k in ("author", "date", "description", "comment")}}
		measurements = []
		for m_def in doc.get("measurements", []):
			f = meta_path.parent / m_def.get("file", "")
			if not f.exists():
				continue
			payload = self._import_file(str(f)) or {}
			measurements.append(MeasurementSeries(
				id=m_def.get("id") or f.stem,
				name=m_def.get("name") or f.stem,
				data=MeasurementData(headers=payload.get("headers") or [], rows=payload.get("rows") or []),
				x=m_def.get("x") or {}, y=m_def.get("y") or {}, plot=m_def.get("plot") or {},
			))
		return Experiment(id=exp_id, metadata=metadata, measurements=measurements)

	def _payload_to_measurement(self, exp_id, payload):
		h = payload.get("headers") or []
		return MeasurementSeries(
			id=f"{exp_id}_measurement_1", name="Messung 1",
			data=MeasurementData(headers=h, rows=payload.get("rows") or []),
			x={"title": h[0] if h else "X", "type": "float", "unit": ""},
			y={"title": h[1] if len(h) > 1 else "Y", "type": "float", "unit": ""},
			plot={"visible": True, "color": "#1f77b4", "line_width": 2},
		)

	def _exp_dir(self, exp_id):
		return Path("data") / "experiments" / exp_id

	def _meas_filename(self, meas):
		return f"{meas.id.replace(' ', '_')}.csv"

	def _write_csv(self, exp_dir, meas):
		self.exporters[0].export_file({"headers": list(meas.data.headers or []), "rows": list(meas.data.rows or [])}, Path(exp_dir) / self._meas_filename(meas))

	def _write_metadata(self, exp):
		d = self._exp_dir(exp.id)
		d.mkdir(parents=True, exist_ok=True)
		meta = exp.metadata or {}
		doc = {
			"experiment": {"id": exp.id, "title": meta.get("title", exp.id), **{k: meta.get(k, "") for k in ("author", "date", "description", "comment")}},
			"measurements": [{"id": m.id, "name": m.name, "file": self._meas_filename(m), "x": dict(m.x or {}), "y": dict(m.y or {}), "plot": dict(m.plot or {})} for m in exp.measurements],
		}
		self.exporters[0].export_file(doc, d / "metadata.json")

	def _persist_experiment(self, exp):
		d = self._exp_dir(exp.id)
		d.mkdir(parents=True, exist_ok=True)
		for m in exp.measurements:
			self._write_csv(d, m)
		self._write_metadata(exp)

	def _new_measurement(self, exp, name=None, headers=None, rows=None):
		h = headers or ["x", "y"]
		idx = len(exp.measurements) + 1
		return MeasurementSeries(
			id=f"{exp.id}_measurement_{idx}", name=name or f"Messreihe {idx}",
			data=MeasurementData(headers=h, rows=rows or []),
			x={"title": h[0], "type": "float", "unit": ""},
			y={"title": h[1] if len(h) > 1 else "Y", "type": "float", "unit": ""},
			plot={"visible": True, "color": "#1f77b4", "line_width": 2},
		)

	def _pick_file(self):
		dialog = ImportDialog(self.main_window)
		return dialog.selected_file_path() if dialog.exec() == QDialog.DialogCode.Accepted else None
