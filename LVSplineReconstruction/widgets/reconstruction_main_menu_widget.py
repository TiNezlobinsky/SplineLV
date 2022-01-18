from math import pi, degrees
from PyQt5 import QtWidgets, QtCore
from GuiStylizedWidgets.coffee_widgets import CoffeeButton


class ReconstructionMainMenuWidget(QtWidgets.QWidget):

    _update_signal = QtCore.pyqtSignal(name="callUpdate")
    _upload_signal = QtCore.pyqtSignal(name="callUpload")
    _construct_diff_mesh_signal = QtCore.pyqtSignal(name="callConstructDiffMesh")
    _export_diff_mesh_signal = QtCore.pyqtSignal(name="callExportDiffMesh")
    _construct_poly_surface_signal = QtCore.pyqtSignal(name="callConstructPolySurface")
    _export_poly_surface_signal = QtCore.pyqtSignal(name="callExportPolySurface")

    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)

        self._parent = parent

        self._main_layer = QtWidgets.QGridLayout()

        self._name_label = QtWidgets.QLabel("Meridians: ", self)
        self._meridians_count_label = QtWidgets.QLabel("0", self)
        self._update_button = CoffeeButton("Update", self)
        self._upload_button = CoffeeButton("Upload", self)
        self._diff_mesh_label = QtWidgets.QLabel("Finite-difference mesh:", self)
        self._construct_diff_mesh_button = CoffeeButton("Construct", self)
        self._export_diff_mesh_button = CoffeeButton("Export", self)
        self._poly_surface_label = QtWidgets.QLabel("Polygonal surface:", self)
        self._construct_poly_surface_button = CoffeeButton("Construct", self)
        self._export_poly_surface_button = CoffeeButton("Export", self)

        self._main_layer.addWidget(self._name_label, 0, 0, 1, 1)
        self._main_layer.addWidget(self._meridians_count_label, 0, 1, 1, 1)
        self._main_layer.addWidget(self._update_button, 1, 0, 1, 1)
        self._main_layer.addWidget(self._upload_button, 1, 1, 1, 1)
        self._main_layer.addWidget(self._diff_mesh_label, 2, 0, 1, 2)
        self._main_layer.addWidget(self._construct_diff_mesh_button, 3, 0, 1, 1)
        self._main_layer.addWidget(self._export_diff_mesh_button, 3, 1, 1, 1)
        self._main_layer.addWidget(self._poly_surface_label, 4, 0, 1, 2)
        self._main_layer.addWidget(self._construct_poly_surface_button, 5, 0, 1, 1)
        self._main_layer.addWidget(self._export_poly_surface_button, 5, 1, 1, 1)

        self.setLayout(self._main_layer)

        self._set_connections()

    def _set_connections(self):
        self._update_button.clicked.connect(self.update_storage_list)
        self._upload_button.clicked.connect(self.upload)
        self._construct_poly_surface_button.clicked.connect(self.construct_poly_surface)
        self._export_poly_surface_button.clicked.connect(self.export_poly_surface)
        self._construct_diff_mesh_button.clicked.connect(self.construct_diff_mesh)
        self._export_diff_mesh_button.clicked.connect(self.export_diff_mesh)

    def set_meridians_list(self, meridians_number):
        self._meridians_count_label.setText(str(meridians_number))

    def update_storage_list(self):
        self._update_signal.emit()

    def upload(self):
        self._upload_signal.emit()

    def construct_diff_mesh(self):
        self._construct_diff_mesh_signal.emit()

    def construct_poly_surface(self):
        self._construct_poly_surface_signal.emit()

    def export_diff_mesh(self):
        self._export_diff_mesh_signal.emit()

    def export_poly_surface(self):
        self._export_poly_surface_signal.emit()
