from PyQt5 import QtWidgets, QtCore
from GuiStylizedWidgets.coffee_widgets import CoffeeColoredButton, CoffeeButton, CoffeeLineEdit


class ImageGeometryWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)

        self._main_layer = QtWidgets.QGridLayout()
        self._set_scale_button = CoffeeColoredButton("red", "Scale", self)
        #self._set_scale_button.setMinimumWidth(50)
        self._h_line_edit = CoffeeLineEdit(self)
        self._set_h_button = CoffeeButton("Set h", self)
        #self._set_h_button.setMinimumWidth(50)
        self._scale_cm_number = QtWidgets.QSpinBox(self)
        self._ruler_button = CoffeeColoredButton("red", "Ruler", self)
        self._level_button = CoffeeColoredButton("red", "Level", self)

        self._main_layer.addWidget(self._set_h_button, 0, 0, 1, 1)
        self._main_layer.addWidget(self._h_line_edit, 0, 1, 1, 2)
        self._main_layer.addWidget(self._level_button, 0, 3, 1, 1)
        self._main_layer.addWidget(self._set_scale_button, 1, 0, 1, 1)
        self._main_layer.addWidget(self._scale_cm_number, 1, 1, 1, 2)
        self._main_layer.addWidget(self._ruler_button, 1, 3, 1, 1)

        self.setLayout(self._main_layer)

        self._set_connections()

        self._engine_manager = None

    def _set_connections(self):
        self._level_button.clicked.connect(self.on_level)
        self._set_h_button.clicked.connect(self.on_set_h)
        self._ruler_button.clicked.connect(self.on_ruler)
        self._set_scale_button.clicked.connect(self.on_set_scale)

    def connect_with_engine_manager(self, engine_manager):
        self._engine_manager = engine_manager

    def on_level(self):
        self._engine_manager.set_image_apex_level_line_state(self._level_button.check_state())

    def on_set_h(self):
        self._engine_manager.set_h()
        self._h_line_edit.setText(str(round(self._engine_manager.get_scaled_h(), 2)))
        if self._engine_manager:
            self._engine_manager.reset_meridians()

    def on_ruler(self):
        self._engine_manager.set_ruler_state(self._ruler_button.check_state())

    def on_set_scale(self):
        self._engine_manager.set_cm_number(int(self._scale_cm_number.text()))
        self._engine_manager.calculate_scale_coeff()
