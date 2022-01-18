from PyQt5 import QtWidgets, QtCore
from GuiStylizedWidgets.coffee_widgets import CoffeeButton, CoffeeColoredButton, CoffeeFullColoredRGBLine, CoffeeColoredRGBButton


class GuiMedianWidget(QtWidgets.QWidget):

    _switch_left_epi_interaction_signal = QtCore.pyqtSignal(name="callSwitchLeftEpiInteraction")
    _switch_left_endo_interaction_signal = QtCore.pyqtSignal(name="callSwitchLeftEndoInteraction")
    _switch_right_epi_interaction_signal = QtCore.pyqtSignal(name="callSwitchRightEpiInteraction")
    _switch_right_endo_interaction_signal = QtCore.pyqtSignal(name="callSwitchRightEndoInteraction")
    _call_left_meridian_signal = QtCore.pyqtSignal(name="callLeftMeridian")
    _call_right_meridian_signal = QtCore.pyqtSignal(name="callRightMeridian")
    _call_reset_left_meridian_signal = QtCore.pyqtSignal(name="callResetLeftMeridian")
    _call_reset_right_meridian_signal = QtCore.pyqtSignal(name="callResetRightMeridian")

    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)

        self._left_meridian_button = CoffeeColoredButton("red", "Left Meridian", self)
        self._right_meridian_button = CoffeeColoredButton("red", "Right Meridian", self)
        self._reset_left_meridian_button = CoffeeButton("Reset", self)
        self._reset_right_meridian_button = CoffeeButton("Reset", self)

        self._initialize_left_median_box()
        self._initialize_right_median_box()

        self._main_layer = QtWidgets.QGridLayout()
        self._main_layer.addWidget(self._left_meridian_button, 0, 0, 1, 1)
        self._main_layer.addWidget(self._reset_left_meridian_button, 0, 1, 1, 1)
        self._main_layer.addWidget(self._right_meridian_button, 1, 0, 1, 1)
        self._main_layer.addWidget(self._reset_right_meridian_button, 1, 1, 1, 1)
        self._main_layer.addWidget(self._left_median_box, 2, 0, 2, 2)
        self._main_layer.addWidget(self._right_median_box, 4, 0, 2, 2)

        self._set_connections()

        self.setLayout(self._main_layer)

        self._engine_manager = None

    def _initialize_left_median_box(self):
        self._left_median_box = QtWidgets.QGroupBox("Left Meridian", self)
        self._manage_left_epi_spline_button = CoffeeColoredRGBButton("127, 127, 255", "Edit epi", self)
        self._manage_left_endo_spline_button = CoffeeColoredRGBButton("255, 51, 153", "Edit endo", self)
        self._left_label_color_epi_spline = CoffeeFullColoredRGBLine("127, 127, 255", self)
        self._left_label_color_endo_spline = CoffeeFullColoredRGBLine("255, 51, 153", self)

        self._left_median_layer = QtWidgets.QGridLayout()
        self._left_median_layer.addWidget(self._manage_left_epi_spline_button, 0, 0)
        self._left_median_layer.addWidget(self._manage_left_endo_spline_button, 0, 1)
        self._left_median_layer.addWidget(self._left_label_color_epi_spline, 1, 0)
        self._left_median_layer.addWidget(self._left_label_color_endo_spline, 1, 1)
        self._left_median_box.setLayout(self._left_median_layer)

    def _initialize_right_median_box(self):
        self._right_median_box = QtWidgets.QGroupBox("Right Meridian", self)
        self._manage_right_epi_spline_button = CoffeeColoredRGBButton("0, 255, 0", "Edit epi", self)
        self._manage_right_endo_spline_button = CoffeeColoredRGBButton("255, 224, 25", "Edit endo", self)
        self._right_label_color_epi_spline = CoffeeFullColoredRGBLine("0, 255, 0", self)
        self._right_label_color_endo_spline = CoffeeFullColoredRGBLine("255, 224, 25", self)

        self._right_median_layer = QtWidgets.QGridLayout()
        self._right_median_layer.addWidget(self._manage_right_epi_spline_button, 0, 0)
        self._right_median_layer.addWidget(self._manage_right_endo_spline_button, 0, 1)
        self._right_median_layer.addWidget(self._right_label_color_epi_spline, 1, 0)
        self._right_median_layer.addWidget(self._right_label_color_endo_spline, 1, 1)
        self._right_median_box.setLayout(self._right_median_layer)

    def _set_connections(self):
        self._manage_left_endo_spline_button.clicked.connect(self.switch_left_endo_interaction_mode)
        self._manage_right_endo_spline_button.clicked.connect(self.switch_right_endo_interaction_mode)
        self._manage_left_epi_spline_button.clicked.connect(self.switch_left_epi_interaction_mode)
        self._manage_right_epi_spline_button.clicked.connect(self.switch_right_epi_interaction_mode)
        self._left_meridian_button.clicked.connect(self.call_left_meridian)
        self._right_meridian_button.clicked.connect(self.call_right_meridian)
        self._reset_left_meridian_button.clicked.connect(self.call_reset_left_meridian)
        self._reset_right_meridian_button.clicked.connect(self.call_reset_right_meridian)

    def connect_with_engine_manager(self, engine_manager):
        self._engine_manager = engine_manager

    def get_right_endo_mode(self):
        return self._manage_right_endo_spline_button.check_state()

    def get_right_epi_mode(self):
        return self._manage_right_epi_spline_button.check_state()

    def get_left_endo_mode(self):
        return self._manage_left_endo_spline_button.check_state()

    def get_left_epi_mode(self):
        return self._manage_left_epi_spline_button.check_state()

    def get_left_meridian_state(self):
        return self._left_meridian_button.check_state()

    def get_right_meridian_state(self):
        return self._right_meridian_button.check_state()

    def set_right_endo_mode(self, state):
        self._manage_right_endo_spline_button.setChecked(state)

    def set_right_epi_mode(self, state):
        self._manage_right_epi_spline_button.setChecked(state)

    def set_left_endo_mode(self, state):
        self._manage_left_endo_spline_button.setChecked(state)

    def set_left_epi_mode(self, state):
        self._manage_left_epi_spline_button.setChecked(state)

    def set_left_meridian_state(self, state):
        self._left_meridian_button.setChecked(state)

    def set_right_meridian_state(self, state):
        self._right_meridian_button.setChecked(state)

    def switch_left_endo_interaction_mode(self):
        self._switch_left_endo_interaction_signal.emit()

    def switch_right_endo_interaction_mode(self):
        self._switch_right_endo_interaction_signal.emit()

    def switch_left_epi_interaction_mode(self):
        self._switch_left_epi_interaction_signal.emit()

    def switch_right_epi_interaction_mode(self):
        self._switch_right_epi_interaction_signal.emit()

    def call_left_meridian(self):
        self._call_left_meridian_signal.emit()

    def call_right_meridian(self):
        self._call_right_meridian_signal.emit()

    def call_reset_left_meridian(self):
        self._call_reset_left_meridian_signal.emit()

    def call_reset_right_meridian(self):
        self._call_reset_right_meridian_signal.emit()
