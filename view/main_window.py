from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMainWindow, QStatusBar, QVBoxLayout, QWidget, QHBoxLayout

from view.partials.toolbar import ToolBar
from view.partials.menubar import MenuBar
from view.app_actions import AppActions
from view.experiment_tree_view import ExperimentTreeView
from view.data_view import DataView
from view.meta_view import MetaView
from view.plot_view import PlotView


class MainWindow(QMainWindow):
    """Assemble the primary application window and child views."""

    def __init__(self, config):
        # Build main frame, actions, and all visible subviews.
        super().__init__()

        # App Config
        app_name = config["app"]["name"]
        app_version = config["app"]["version"]
        window_width = config["ui"]["window_width"]
        window_height = config["ui"]["window_height"]

        self.setWindowTitle(app_name + " - " + app_version)
        self.setFixedSize(window_width, window_height)

        self.actions = AppActions(self)

        # Menubar
        self.menu_bar = MenuBar(self.actions, self)
        self.setMenuBar(self.menu_bar)

        # Toolbar
        toolbar = ToolBar(self.actions, self)
        self.addToolBar(toolbar)

        # Sidebar
        self.experiment_tree_view = ExperimentTreeView(self)
        self.addDockWidget(
            Qt.DockWidgetArea.LeftDockWidgetArea,
            self.experiment_tree_view
        )

        # Statusbar
        self.setStatusBar(QStatusBar(self))

        # Main
        container = QWidget()
        self.setCentralWidget(container)

        # Metainformationen
        self.meta_view = MetaView()

        # Messdaten
        self.data_view = DataView()

        # Plot
        self.plot_view = PlotView()

        # Layout stacks metadata above a data table and live plot.
        data_layout = QHBoxLayout()
        data_layout.addWidget(self.data_view)
        data_layout.addWidget(self.plot_view)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.meta_view)
        main_layout.addLayout(data_layout)

        container.setLayout(main_layout)

    def set_experiment_tree_model(self, model):
        # Forward tree model binding to the sidebar view.
        self.experiment_tree_view.set_model(model)

    def set_measurement_model(self, model):
        # Forward measurement model binding to the data view.
        self.data_view.set_model(model)

    def set_meta(self, metadata):
        # Push experiment metadata fields to the metadata widget.
        self.meta_view.set_meta(
            title=metadata.get("title", ""),
            author=metadata.get("author", ""),
            date=metadata.get("date", ""),
            description=metadata.get("description", ""),
            comment=metadata.get("comment", ""),
        )

    def set_plots(self, series_list, title="", label_x="", label_y="", unit_x="", unit_y=""):
        # Push plot-ready series and labels to the plot widget.
        self.plot_view.set_plots(
            series_list,
            title=title,
            label_x=label_x,
            label_y=label_y,
            unit_x=unit_x,
            unit_y=unit_y,
        )