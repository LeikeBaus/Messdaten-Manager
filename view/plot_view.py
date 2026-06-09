import os
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QFileDialog, QMessageBox
import pyqtgraph as pg
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


        self.export_btn = QPushButton("Export Plot as PNG")
        self.export_btn.clicked.connect(self.on_export_clicked)
        layout.addWidget(self.export_btn)

        self.setLayout(layout)

    def create_demo_plot(self):
        """Erstellt man einen einfachen Plot zu ausgeben."""
        import numpy as np
        x = np.linspace(0, 10, 100)
        y = np.sin(x)
        self.plot_widget.plot(x, y, pen='b')

    def on_export_clicked(self):
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

        # Verwalte der Kontroller
        success = self.controller.export_plot(self.plot_widget, file_path)
        if success:
            QMessageBox.information(self, "Success", f"Plot saved to:\n{file_path}")
        else:
            QMessageBox.critical(self, "Error", "Failed to export plot.")