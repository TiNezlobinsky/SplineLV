from PyQt5 import QtWidgets, QtCore
from GuiStylizedWidgets.coffee_widgets import CoffeeColoredButton, CoffeeButton, CoffeeLineEdit


class MeshGeometryWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)

        self._main_layer = QtWidgets.QGridLayout()
        self._h_line_edit = CoffeeLineEdit(self)
        self._set_h_button = CoffeeButton("Set h", self)
        self._level_button = CoffeeColoredButton("red", "Level", self)

        self._main_layer.addWidget(self._set_h_button, 0, 0, 1, 1)
        self._main_layer.addWidget(self._h_line_edit, 0, 1, 1, 2)
        self._main_layer.addWidget(self._level_button, 0, 3, 1, 1)

        self.setLayout(self._main_layer)

        self._engine_manager = None

        self._set_connections()

    def _set_connections(self):
        self._level_button.clicked.connect(self.on_level_button)
        self._set_h_button.clicked.connect(self.on_set_h_button)

    def connect_with_engine_manager(self, engine_manager):
        self._engine_manager = engine_manager

    def on_level_button(self):
        self._engine_manager.set_mesh_apex_level_line_state(self._level_button.check_state())

    def on_set_h_button(self):
        self._engine_manager.set_h()
        self._h_line_edit.setText(str(self._engine_manager.get_h()))
