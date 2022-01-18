from PyQt5 import QtWidgets, QtCore
from GuiStylizedWidgets.coffee_widgets import CoffeeButton, CoffeeListWidget, CoffeeLineEdit


class DataControlWidget(QtWidgets.QWidget):

    _load_signal = QtCore.pyqtSignal(name="callLoad")
    _switch_row_signal = QtCore.pyqtSignal(int, name="callSwitchRow")
    _upload_signal = QtCore.pyqtSignal(name="callUpload")

    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)

        self._load_directory_button = CoffeeButton("Load", self)
        self._upload_button = CoffeeButton("Upload", self)
        self._snapshot_button = CoffeeButton("Snapshot", self)
        self._main_layer = QtWidgets.QGridLayout()
        self._load_directory_line = CoffeeLineEdit(self)
        self._slice_ListWidget = CoffeeListWidget(self)
        self._main_layer.addWidget(self._load_directory_line, 0, 0, 1, 3)
        self._main_layer.addWidget(self._slice_ListWidget, 1, 0, 4, 3)
        self._main_layer.addWidget(self._load_directory_button, 5, 0, 1, 1)
        self._main_layer.addWidget(self._upload_button, 5, 1, 1, 1)
        self._main_layer.addWidget(self._snapshot_button, 5, 2, 1, 1)

        self.setLayout(self._main_layer)

        self._engine_manager = None

        self._local_storage = None

        self._parent = parent  # reference to MeasurementWidget class object

        self._set_connections()

    def _set_connections(self):
        self._load_directory_button.clicked.connect(self.load)
        self._upload_button.clicked.connect(self.upload)
        self._slice_ListWidget.itemClicked.connect(self.switch_row)

    def connect_with_engine_manager(self, engine_manager):
        self._engine_manager = engine_manager

    def connect_with_local_strorage(self, local_storage):
        self._local_storage = local_storage

    def add_rows_to_list_widget(self, file_name_list):
        items_list = []
        self._slice_ListWidget.clear()
        for i, file_name in enumerate(file_name_list):
            items_list.append(QtWidgets.QListWidgetItem())
            items_list[i].setText(file_name)
            self._slice_ListWidget.insertItem(i, items_list[i])

    def set_text_to_load_line(self, folder_name):
        self._load_directory_line.setText(folder_name)

    def load(self):
        self._load_signal.emit()

    def switch_row(self, item):
        row = self._slice_ListWidget.row(item)
        self._switch_row_signal.emit(row)

    def upload(self):
        self._upload_signal.emit()
