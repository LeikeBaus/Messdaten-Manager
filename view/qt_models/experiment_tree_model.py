from PyQt6.QtCore import Qt
from PyQt6.QtGui import QStandardItem, QStandardItemModel


NODE_TYPE_ROLE = int(Qt.ItemDataRole.UserRole) + 1
EXPERIMENT_ID_ROLE = int(Qt.ItemDataRole.UserRole) + 2
MEASUREMENT_ID_ROLE = int(Qt.ItemDataRole.UserRole) + 3

NODE_TYPE_EXPERIMENT = "experiment"
NODE_TYPE_MEASUREMENT = "measurement"


class ExperimentTreeModel(QStandardItemModel):
    def __init__(self, experiments=None):
        super().__init__()
        self.setHorizontalHeaderLabels(["Experimente und Messreihen"])
        self._experiments = []
        self.set_experiments(experiments or [])

    def set_experiments(self, experiments):
        self._experiments = list(experiments)
        self.clear()
        self.setHorizontalHeaderLabels(["Experimente und Messreihen"])

        for experiment in self._experiments:
            title = experiment.metadata.get("title", experiment.id)
            experiment_item = QStandardItem(title)
            experiment_item.setEditable(False)
            experiment_item.setData(NODE_TYPE_EXPERIMENT, NODE_TYPE_ROLE)
            experiment_item.setData(experiment.id, EXPERIMENT_ID_ROLE)

            for measurement in experiment.measurements:
                measurement_item = QStandardItem(measurement.name)
                measurement_item.setEditable(False)
                measurement_item.setData(NODE_TYPE_MEASUREMENT, NODE_TYPE_ROLE)
                measurement_item.setData(experiment.id, EXPERIMENT_ID_ROLE)
                measurement_item.setData(measurement.id, MEASUREMENT_ID_ROLE)
                experiment_item.appendRow(measurement_item)

            self.appendRow(experiment_item)

    def item_info(self, index):
        if not index.isValid():
            return None

        node_type = index.data(NODE_TYPE_ROLE)
        experiment_id = index.data(EXPERIMENT_ID_ROLE)
        measurement_id = index.data(MEASUREMENT_ID_ROLE)

        if node_type == NODE_TYPE_EXPERIMENT:
            return {
                "type": NODE_TYPE_EXPERIMENT,
                "experiment_id": experiment_id,
            }

        if node_type == NODE_TYPE_MEASUREMENT:
            return {
                "type": NODE_TYPE_MEASUREMENT,
                "experiment_id": experiment_id,
                "measurement_id": measurement_id,
            }

        return None
