from PyQt5 import QtWidgets, QtCore
from GuiStylizedWidgets.coffee_widgets import CoffeeButton, CoffeeColoredButton, CoffeeLineEdit


class VarZParametersBox(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)

        self._mesh_wall_label = QtWidgets.QLabel("Wall (psi):", self)
        self._mesh_wall_edit = CoffeeLineEdit(self)
        self._mesh_wall_edit.setText("60")
        self._mesh_wall_edit.setAlignment(QtCore.Qt.AlignCenter)
        self._mesh_surface_label = QtWidgets.QLabel("Surface (phi):", self)
        self._mesh_surface_edit = CoffeeLineEdit(self)
        self._mesh_surface_edit.setText("60")
        self._mesh_surface_edit.setAlignment(QtCore.Qt.AlignCenter)
        self._mesh_layers_label = QtWidgets.QLabel("Layers (gamma):", self)
        self._mesh_layers_edit = CoffeeLineEdit(self)
        self._mesh_layers_edit.setText("3")
        self._mesh_layers_edit.setAlignment(QtCore.Qt.AlignCenter)
        self._main_layer = QtWidgets.QGridLayout()
        self._gamma_0_label = QtWidgets.QLabel("Gamma 0:", self)
        self._gamma_0_edit = CoffeeLineEdit(self)
        self._gamma_0_edit.setText("0.0")
        self._gamma_0_edit.setAlignment(QtCore.Qt.AlignCenter)
        self._gamma_1_label = QtWidgets.QLabel("Gamma 1:", self)
        self._gamma_1_edit = CoffeeLineEdit(self)
        self._gamma_1_edit.setText("1.0")
        self._gamma_1_edit.setAlignment(QtCore.Qt.AlignCenter)

        self._main_layer.addWidget(self._mesh_wall_label, 0, 0)
        self._main_layer.addWidget(self._mesh_wall_edit, 0, 1)
        self._main_layer.addWidget(self._mesh_surface_label, 1, 0)
        self._main_layer.addWidget(self._mesh_surface_edit, 1, 1)
        self._main_layer.addWidget(self._mesh_layers_label, 2, 0)
        self._main_layer.addWidget(self._mesh_layers_edit, 2, 1)
        self._main_layer.addWidget(self._gamma_0_label, 3, 0)
        self._main_layer.addWidget(self._gamma_0_edit, 3, 1)
        self._main_layer.addWidget(self._gamma_1_label, 4, 0)
        self._main_layer.addWidget(self._gamma_1_edit, 4, 1)

        self.setLayout(self._main_layer)

        self._main_layer.setContentsMargins(0, 0, 0, 0)

    def get_wall_points(self):
        # need try - except here
        return int(self._mesh_wall_edit.text())

    def get_surface_points(self):
        # need try - except here
        return int(self._mesh_surface_edit.text())

    def get_layers_number(self):
        # need try - except here
        return int(self._mesh_layers_edit.text())

    def get_gamma_0(self):
        # need try - except here
        return float(self._gamma_0_edit.text())

    def get_gamma_1(self):
        # need try - except here
        return float(self._gamma_1_edit.text())