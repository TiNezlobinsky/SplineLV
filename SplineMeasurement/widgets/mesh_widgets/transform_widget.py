from PyQt5 import QtWidgets, QtCore
from GuiStylizedWidgets.coffee_widgets import CoffeeButton, CoffeeLineEdit


class TransformWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)

        self._angle_value_edit = CoffeeLineEdit(self)
        self._angle_value_edit.setAlignment(QtCore.Qt.AlignCenter)
        self._angle_value_edit.setText("90")
        self._rotate_x_button = CoffeeButton("Rotate x", self)
        self._rotate_y_button = CoffeeButton("Rotate y", self)
        self._rotate_z_button = CoffeeButton("Rotate z", self)

        self._main_layer = QtWidgets.QGridLayout()
        self._main_layer.addWidget(self._rotate_x_button, 0, 0, 1, 2)
        self._main_layer.addWidget(self._angle_value_edit, 0, 2, 1, 2)
        self._main_layer.addWidget(self._rotate_y_button, 1, 0, 1, 2)
        self._main_layer.addWidget(self._rotate_z_button, 1, 2, 1, 2)

        self.setLayout(self._main_layer)

        self._engine_manager = None

        self._set_connections()

    def _set_connections(self):
        self._rotate_x_button.clicked.connect(self.rotate_x)
        self._rotate_y_button.clicked.connect(self.rotate_y)
        self._rotate_z_button.clicked.connect(self.rotate_z)
        
    def connect_with_engine_manager(self, engine_manager):
        self._engine_manager = engine_manager

    def rotate_x(self):
        # need try - except here
        self._engine_manager.rotate_x(float(self._angle_value_edit.text()))

    def rotate_y(self):
        # need try - except here
        self._engine_manager.rotate_y(float(self._angle_value_edit.text()))

    def rotate_z(self):
        # need try - except here
        self._engine_manager.rotate_z(float(self._angle_value_edit.text()))
