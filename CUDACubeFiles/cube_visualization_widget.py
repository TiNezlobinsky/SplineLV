from PyQt5 import QtWidgets, QtCore

from CUDACubeFiles.cube_engine_manager import CubeEngineManager
from GuiStylizedWidgets.coffee_widgets import CoffeeButton, CoffeeLineEdit
from CUDACubeFiles.engine.vtk_cube_scene import VtkCubeScene


class CubeVisualizationWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)

        self._initialize_cube_parameters_box()
        self._initialize_vtk_scene_widget()
        # self._initialize_panel()

        self._main_layer = QtWidgets.QHBoxLayout()
        self._main_layer.addWidget(self._vtk_frame, 4)
        self._main_layer.addWidget(self._cube_parameters_box, 1)
        self.setLayout(self._main_layer)

        self._set_connections()

        self._storage_regist_key = "CUDACubes"

    def connect_with_storage(self, local_storage):
        """
        Connect with the local storage to data exchange between packages

        Parameters
        ----------
        local_storage : object
            LocalStorage class object
        """
        self._local_storage = local_storage

    def _set_connections(self):
        self._generate_button.clicked.connect(self.generate_cube)
        self._upload_button.clicked.connect(self.upload)

        # self.connect(self._generate_button, QtCore.SIGNAL("clicked(bool)"),
        #             self.generate_cube)
        # self.connect(self._upload_button, QtCore.SIGNAL("clicked(bool)"),
        #             self.upload)

    def _initialize_cube_parameters_box(self):
        self._cube_parameters_box = QtWidgets.QGroupBox("Cube parameters", self)
        self._cube_parameters_layer = QtWidgets.QGridLayout()

        self._side_n_label = QtWidgets.QLabel("Side (n):", self)
        self._side_n_edit = CoffeeLineEdit(self)
        self._side_n_edit.setText("100")
        self._side_n_edit.setAlignment(QtCore.Qt.AlignCenter)
        self._x0cube_label = QtWidgets.QLabel("x0 cube:", self)
        self._x0cube_edit = CoffeeLineEdit(self)
        self._x0cube_edit.setText("-50")
        self._x0cube_edit.setAlignment(QtCore.Qt.AlignCenter)
        self._y0cube_label = QtWidgets.QLabel("y0 cube:", self)
        self._y0cube_edit = CoffeeLineEdit(self)
        self._y0cube_edit.setText("-50")
        self._y0cube_edit.setAlignment(QtCore.Qt.AlignCenter)
        self._z0cube_label = QtWidgets.QLabel("z0 cube:", self)
        self._z0cube_edit = CoffeeLineEdit(self)
        self._z0cube_edit.setText("-5")
        self._z0cube_edit.setAlignment(QtCore.Qt.AlignCenter)
        self._dr_label = QtWidgets.QLabel("dr:", self)
        self._dr_edit = CoffeeLineEdit(self)
        self._dr_edit.setText("1.0")
        self._dr_edit.setAlignment(QtCore.Qt.AlignCenter)
        self._distance_label = QtWidgets.QLabel("distance:", self)
        self._distance_edit = CoffeeLineEdit(self)
        self._distance_edit.setText("1.0")
        self._distance_edit.setAlignment(QtCore.Qt.AlignCenter)

        self._button_box = QtWidgets.QGroupBox("")
        self._button_layer = QtWidgets.QGridLayout()
        self._update_button = QtWidgets.QPushButton("Update", self)
        self._upload_button = QtWidgets.QPushButton("Upload", self)
        self._generate_button = QtWidgets.QPushButton("Generate", self)
        self._export_button = QtWidgets.QPushButton("Export", self)
        self._button_layer.addWidget(self._update_button, 0, 0)
        self._button_layer.addWidget(self._upload_button, 0, 1)
        self._button_layer.addWidget(self._generate_button)
        self._button_layer.addWidget(self._export_button)
        self._button_box.setLayout(self._button_layer)

        self._cube_parameters_layer.addWidget(self._side_n_label, 0, 0, 1, 2)
        self._cube_parameters_layer.addWidget(self._side_n_edit, 0, 2, 1, 2)
        self._cube_parameters_layer.addWidget(self._x0cube_label, 1, 0, 1, 2)
        self._cube_parameters_layer.addWidget(self._x0cube_edit, 1, 2, 1, 2)
        self._cube_parameters_layer.addWidget(self._y0cube_label, 2, 0, 1, 2)
        self._cube_parameters_layer.addWidget(self._y0cube_edit, 2, 2, 1, 2)
        self._cube_parameters_layer.addWidget(self._z0cube_label, 3, 0, 1, 2)
        self._cube_parameters_layer.addWidget(self._z0cube_edit, 3, 2, 1, 2)
        self._cube_parameters_layer.addWidget(self._dr_label, 4, 0, 1, 2)
        self._cube_parameters_layer.addWidget(self._dr_edit, 4, 2, 1, 2)
        self._cube_parameters_layer.addWidget(self._distance_label, 5, 0, 1, 2)
        self._cube_parameters_layer.addWidget(self._distance_edit, 5, 2, 1, 2)
        self._cube_parameters_layer.addWidget(self._button_box, 6, 0, 1, 4)
        self._cube_parameters_layer.setRowStretch(7, 1)

        self._cube_parameters_box.setLayout(self._cube_parameters_layer)

    def _initialize_panel(self):
        self._panel_layer = QtWidgets.QVBoxLayout()
        self._panel_layer.addWidget(self._cube_parameters_box)

    def _initialize_vtk_scene_widget(self):
        self._vtk_frame = QtWidgets.QFrame()

        vtk_scene = VtkCubeScene(self._vtk_frame)

        self._vtk_layer = QtWidgets.QVBoxLayout()
        self._vtk_layer.addWidget(vtk_scene)
        self._vtk_frame.setLayout(self._vtk_layer)

        self._engine_manager = CubeEngineManager()
        self._engine_manager.connect_with_scene(vtk_scene)

    def start_vtk_scene(self):
        self._engine_manager.run_the_scene()

    def read_parameters(self):
        # need try - except here or type checking
        parameters_dict = {}
        parameters_dict["n_side"] = int(self._side_n_edit.text())
        parameters_dict["x0cube"] = int(self._x0cube_edit.text())
        parameters_dict["y0cube"] = int(self._y0cube_edit.text())
        parameters_dict["z0cube"] = int(self._z0cube_edit.text())
        parameters_dict["dr"] = float(self._dr_edit.text())
        parameters_dict["distance"] = float(self._distance_edit.text())

        return parameters_dict

    def generate_cube(self):
        self._engine_manager.set_parameters(self.read_parameters())
        self.get_mesh()
        self._engine_manager.set_cube_size(int(self._side_n_edit.text()))
        self._engine_manager.generate()

    def get_mesh(self):
        data_dict = self._local_storage.get_access(self._storage_regist_key)
        self._engine_manager.set_data_dict(data_dict)

    def upload(self):
        self._local_storage.upload_data(self._storage_regist_key,
                                        self._engine_manager.get_arrays())
