from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMainWindow, QStatusBar, QPushButton, QVBoxLayout, QTableWidget, QWidget, QHBoxLayout

from view.partials.toolbar import ToolBar
from view.partials.sidebar import SideBar
from view.partials.menubar import MenuBar
from view.widgets.data_widget import DataWidget

# Tests (evtl. anschließend entfernen)
from view.widgets.meta_widget import MetaWidget
from view.widgets.plot_widget import PlotWidget


class MainWindow(QMainWindow):
    def __init__(self, config):
        super().__init__()

        # App Config
        app_name = config["app"]["name"]
        app_version = config["app"]["version"]
        window_width = config["ui"]["window_width"]
        window_height = config["ui"]["window_height"]

        self.setWindowTitle(app_name + " - " + app_version)
        self.setFixedSize(window_width, window_height)

        # Menubar
        self.menuBar = MenuBar(self)

        # Toolbar
        toolbar = ToolBar(self)
        self.addToolBar(toolbar)

        # Sidebar
        self.sidebar = SideBar(self)
        self.addDockWidget(
            Qt.DockWidgetArea.LeftDockWidgetArea,
            self.sidebar
        )

        # Statusbar
        self.setStatusBar(QStatusBar(self))

        # Main
        container = QWidget()
        self.setCentralWidget(container)

        # Metainformationen
        self.meta_widget = MetaWidget()
        # Setzen der Daten Bsp.
        self.meta_widget.set_meta("Marcel Bartneck")

        # Bsp. Daten
        hour = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        temperature = [30, 32, 34, 32, 33, 31, 29, 32, 35, 45]

        # CSV Daten
        self.data_widget = DataWidget()
        self.data_widget.set_data(hour, temperature)

        # Plot
        self.plot_widget = PlotWidget()
        self.plot_widget.set_plot(hour, temperature)

        data_layout = QHBoxLayout()
        data_layout.addWidget(self.data_widget)
        data_layout.addWidget(self.plot_widget)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.meta_widget)
        main_layout.addLayout(data_layout)

        container.setLayout(main_layout)