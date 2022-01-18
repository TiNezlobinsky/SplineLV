from PyQt5 import QtWidgets, QtCore
from GuiStylizedWidgets.coffee_widgets import CoffeeButton, CoffeeColoredButton


class PositioningWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)

        self._marking_button = CoffeeColoredButton("red", "Marking", self)
        #self._marking_button.setMinimumWidth(120)
        self._remove_marks_button = CoffeeButton("Remove")
        #self._remove_marks_button.setMinimumWidth(120)
        self._align_button = CoffeeButton("Set")
        #self._align_button.setMinimumWidth(120)
        self._label_lines_visibility_button = CoffeeColoredButton("red", "Visible", self)
        #self._label_lines_visibility_button.setMinimumWidth(120)

        self._positioning_layer = QtWidgets.QGridLayout()

        self._positioning_layer.addWidget(self._marking_button, 0, 0, 1, 2)
        self._positioning_layer.addWidget(self._remove_marks_button, 0, 2, 1, 2)
        self._positioning_layer.addWidget(self._align_button, 1, 0, 1, 2)
        self._positioning_layer.addWidget(self._label_lines_visibility_button, 1, 2, 1, 2)

        self.setLayout(self._positioning_layer)

        self._engine_manager = None

        self._set_connections()

    def _set_connections(self):
        self._marking_button.clicked.connect(self.on_marking_button)
        self._remove_marks_button.clicked.connect(self.on_remove_button)
        self._align_button.clicked.connect(self.rotate_image)
        self._label_lines_visibility_button.clicked.connect(self.on_visible_button)

    def connect_with_engine_manager(self, engine_manager):
        self._engine_manager = engine_manager

    def on_marking_button(self):
        self._engine_manager.set_marking_state(self._marking_button.check_state())

    def on_remove_button(self):
        self._engine_manager.remove_marks()

    def on_set_button(self):
        pass

    def on_visible_button(self):
        self._engine_manager.set_label_lines_visibility_state(self._label_lines_visibility_button.check_state())

    def rotate_image(self):
        self._engine_manager.rotate_image_to_axis()
