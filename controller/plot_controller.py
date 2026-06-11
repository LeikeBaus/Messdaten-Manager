from pyqtgraph.exporters import ImageExporter

class PlotController:
    def __init__(self, view):
        self.view = view

    def export_plot(self, plot_widget, file_path):
        """Exportiert man einen Png Ordner Dateils"""
        try:
            exporter = ImageExporter(plot_widget.plotItem)
            exporter.export(file_path)
            return True
        except Exception as e:
            print(f"Export error: {e}")
            return False