import os
from datetime import datetime
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QCheckBox, QFileDialog, QMessageBox, QApplication
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QGuiApplication, QPixmap
import pyqtgraph as pg
import tempfile
from controller.plot_controller import PlotController

class PlotView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.controller = PlotController(self)
        self.init_ui()
        self.create_demo_plot()
    # Erstelle Layouts
    def init_ui(self):
        layout = QVBoxLayout()

        # Definere pg als PlotWidget
        self.plot_widget = pg.PlotWidget()
        layout.addWidget(self.plot_widget)
	
	#Layout des Buttons (Horizontal)
	button_layout = QHBoxLayout()
        self.export_btn = QPushButton("Export Plot as PNG")
	self.copy_btn = QPushButton("Copy to Clipboard")
	self.transparent_cb = QCheckBox("Transparent background")
	button_layout.addWidget(self.export_btn)
	button_layout.addWidget(self.copy_btn)
	button_layout.addWidget(self.transparent_cb)
	layout.addLayout(button_layout)

	self.setLayout(layout)

	#Verbindet man die Signalen
	self.export_btn.clicked.connect(self.on_export_clicked)
	self.copy_btn.clicked.connect(self.on_copy_clicked)

    def create_demo_plot(self):
        """Erstellt man einen einfachen Plot zu ausgeben."""
        import numpy as np
        x = np.linspace(0, 10, 100)
        y = np.sin(x)
        self.plot_widget.plot(x, y, pen='b')

    def on_export_clicked(self):
	# Smart Dateinamen
	default_name = f"plot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
	default_path = os.path.join(os.path.expanduser("~"), default_name)

        """Es ruft auf, wenn export button gedruckt hat"""
        # Offene Dialog Box
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Plot as PNG",
            os.path.expanduser("~"),
            "PNG Images (*.png)"
        )
        if not file_path:
            return
        # versichere .png extension
        if not file_path.lower().endswith('.png'):
            file_path += '.png'

	transparent = self.transparent_cb.isChecked()

	#Zeigt es sich Warte Cursor wahrend des Exports
	QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
	try:
	    success = self.controller.export_plot(self.plot_widget, file_path, transparent=transparent)
	finally:
	    QApplication.restoreOverrideCursor()


        # Verwalte der Kontroller
        success = self.controller.export_plot(self.plot_widget, file_path)
        if success:
            QMessageBox.information(self, "Success", f"Plot saved to:\n{file_path}")
        else:
            QMessageBox.critical(self, "Error", "Failed to export plot.")
