class SelectionContext:
    """Expose normalized selection information from the experiment tree."""

    def __init__(self, experiment_list_view, experiment_tree_model):
        # Keep references required to resolve selected nodes.
        self.experiment_list_view = experiment_list_view
        self.experiment_tree_model = experiment_tree_model

    def selected_node_info(self):
        # Return normalized node metadata for controller decisions.
        index = self.experiment_list_view.selected_index()
        if index is None:
            return None
        return self.experiment_tree_model.item_info(index)

    def selected_experiment_id(self):
        # Return selected experiment id only for experiment nodes.
        info = self.selected_node_info()
        if info is None or info["type"] != "experiment":
            return None
        return info["experiment_id"]

    def selected_measurement_ref(self):
        # Return selected experiment/measurement ids for measurement nodes.
        info = self.selected_node_info()
        if info is None or info["type"] != "measurement":
            return None
        return info
