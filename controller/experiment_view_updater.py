class ExperimentViewUpdater:
    """Update table, metadata, and plot widgets from selected entities."""

    def __init__(self, main_window, measurement_table_model):
        # Store view references used for synchronized UI updates.
        self.main_window = main_window
        self.measurement_table_model = measurement_table_model

    def clear(self):
        # Reset all detail views when no valid selection is available.
        self.measurement_table_model.set_measurements([], [])
        self.main_window.set_meta({})
        self.main_window.set_plots([], title="", label_x="", label_y="")

    def show_experiment(self, experiment):
        # Render metadata plus all plottable measurement series.
        if experiment is None:
            self.clear()
            return

        first_measurement = experiment.measurements[0] if experiment.measurements else None

        if first_measurement is None:
            self.measurement_table_model.set_measurements([], [])
        else:
            self.measurement_table_model.set_measurements(first_measurement.data.headers, first_measurement.data.rows)

        self.main_window.set_meta(experiment.metadata)
        # Show all plottable series when the experiment node is selected.
        plot_series = self.visible_plot_series(experiment)

        label_x = "X"
        label_y = "Y"
        unit_x = ""
        unit_y = ""
        if first_measurement is not None:
            label_x = first_measurement.x.get("title", "X")
            label_y = first_measurement.y.get("title", "Y")
            unit_x = first_measurement.x.get("unit", "")
            unit_y = first_measurement.y.get("unit", "")

        title = experiment.metadata.get("title", experiment.id)
        self.main_window.set_plots(plot_series, title=title, label_x=label_x, label_y=label_y, unit_x=unit_x, unit_y=unit_y)

    def show_measurement(self, experiment, measurement):
        # Render metadata plus exactly one selected measurement series.
        if experiment is None or measurement is None:
            self.clear()
            return

        plot_series = [self._to_plot_series(measurement)]

        self.measurement_table_model.set_measurements(measurement.data.headers, measurement.data.rows)
        self.main_window.set_meta(experiment.metadata)
        self.main_window.set_plots(
            plot_series,
            title=experiment.metadata.get("title", experiment.id),
            label_x=measurement.x.get("title", "X"),
            label_y=measurement.y.get("title", "Y"),
            unit_x=measurement.x.get("unit", ""),
            unit_y=measurement.y.get("unit", ""),
        )

    def visible_plot_series(self, experiment):
        # Build a list of plot-ready series from experiment measurements.
        plot_series = []
        for measurement in experiment.measurements:
            x_values, y_values = measurement.data.numeric_xy_series()
            if not x_values or not y_values:
                continue
            plot_series.append(self._to_plot_series(measurement, x_values, y_values))
        return plot_series

    def _to_plot_series(self, measurement, x_values=None, y_values=None):
        # Map a MeasurementSeries into the plot widget data contract.
        if x_values is None or y_values is None:
            x_values, y_values = measurement.data.numeric_xy_series()

        return {
            "name": measurement.name,
            "x": x_values,
            "y": y_values,
            "color": measurement.plot.get("color", "#1f77b4"),
            "line_width": measurement.plot.get("line_width", 2),
        }
