from PyQt5 import QtWidgets, QtCore
from local_storage import LocalStorage

# Packages:
from SplineMeasurement.measurement_widget import MeasurementWidget
from LVSplineReconstruction.reconstruction_widget import ReconstructionWidget
from CUDACubeFiles.cube_visualization_widget import CubeVisualizationWidget
from DiffuseFibrosis.diff_fibrosis_widget import DiffFibrosisWidget


class MainFrame(QtWidgets.QMainWindow):
    """
    Frame to including package's widgets.
    Uses tabs to represents every package
    """
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)

        self._data_store = LocalStorage()

        self._tab_frame_widget = QtWidgets.QTabWidget()

        self._initialize_packages()
        self._initialize_tab_widgets_list()

        self.setCentralWidget(self._tab_frame_widget)

    def _initialize_packages(self):
        self._measurement_widget = MeasurementWidget(self)
        self._measurement_widget.start_vtk_scene()
        self._measurement_widget.connect_with_storage(self._data_store)

        self._reconstruction_widget = ReconstructionWidget(self)
        self._reconstruction_widget.start_vtk_scene()
        self._reconstruction_widget.connect_with_storage(self._data_store)

        self._cube_visualization_widget = CubeVisualizationWidget(self)
        self._cube_visualization_widget.start_vtk_scene()
        self._cube_visualization_widget.connect_with_storage(self._data_store)

        self._diff_fibrosis_widget = DiffFibrosisWidget(self)
        self._diff_fibrosis_widget.start_vtk_scene()
        self._diff_fibrosis_widget.connect_with_storage(self._data_store)

    def _initialize_tab_widgets_list(self):
        self._tab_frame_widget.addTab(self._measurement_widget, "SliceProcessing")
        self._tab_frame_widget.addTab(self._reconstruction_widget, "Reconstruction")
        self._tab_frame_widget.addTab(self._cube_visualization_widget, "CubeGenerator")
        self._tab_frame_widget.addTab(self._diff_fibrosis_widget, "DiffFibrosis")


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)

    frame_widget = MainFrame()

    main_window = QtWidgets.QMainWindow()
    main_window.setCentralWidget(frame_widget)
    main_window.show()

    sys.exit(app.exec_())
