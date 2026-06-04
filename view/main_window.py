from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMainWindow, QStatusBar, QPushButton, QVBoxLayout, QTableWidget

from view.partials.toolbar import ToolBar
from view.partials.sidebar import SideBar
from view.partials.menubar import MenuBar

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
        # ToDo
        #   - Infofelder
        #   - Datentabelle
        #   - Plot
