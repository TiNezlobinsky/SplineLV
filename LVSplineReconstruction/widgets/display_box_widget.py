from PyQt5 import QtWidgets, QtCore
from GuiStylizedWidgets.coffee_widgets import CoffeeButton, CoffeeColoredButton, CoffeeLineEdit


class DisplayBoxWidget(QtWidgets.QWidget):

    #
    _set_opacity_signal = QtCore.pyqtSignal(int, name="callSetOpacity")
    _set_visual_object_signal = QtCore.pyqtSignal(str, name="callSetVisualObject")

    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)

        self._main_layer = QtWidgets.QGridLayout()

        self._display_list_box = QtWidgets.QComboBox(self)
        self._initialize_display_list_box()
        self._visualize_mesh_button = CoffeeColoredButton("red", "Mesh", self)
        self._visualize_fibers_button = CoffeeColoredButton("red", "Fibers", self)
        self._opacity_slider = QtWidgets.QSlider(self)
        self._opacity_slider.setMaximum(100)  # to make range richer
        self._opacity_slider.setOrientation(QtCore.Qt.Horizontal)

        self._main_layer.addWidget(self._display_list_box, 0, 0, 1, 2)
        self._main_layer.addWidget(self._visualize_mesh_button, 1, 0, 1, 1)
        self._main_layer.addWidget(self._visualize_fibers_button, 1, 1, 1, 1)
        self._main_layer.addWidget(self._opacity_slider, 2, 0, 1, 2)

        self.setLayout(self._main_layer)

        self._set_connections()

        self._main_layer.setContentsMargins(0, 0, 0, 0)

    def _set_connections(self):
        self._opacity_slider.valueChanged.connect(self.set_opacity_value)
        self._display_list_box.currentIndexChanged.connect(self.set_visual_object)

    def _initialize_display_list_box(self):
        self._display_list_box.addItem("FiniteDiffMesh")
        self._display_list_box.addItem("FiniteElemSurface")
        self._display_list_box.addItem("FibersField")

    def set_visual_object(self, text):
        self._set_visual_object_signal.emit(text)

    def set_opacity_value(self, i):
        self._set_opacity_signal.emit(i)  # should be float
