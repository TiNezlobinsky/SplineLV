from PyQt5 import QtWidgets, QtCore
from DiffuseFibrosis.engine.vtk_diff_fibrosis_scene import VtkDiffFibrosisScene
from DiffuseFibrosis.diff_fibrosis_engine_manager import DiffFibrosisEngineManager


class DiffFibrosisWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)

        self._initialize_vtk_scene_widget()

        self._initialize_uniform_points_widget()
        self._initialize_uniform_twigs_widget()
        self._initialize_distribution_box()
        self._initialize_control_box()
        self._initialize_panel_widget()

        self._distribution_stack.setCurrentIndex(0)

        self._main_layer = QtWidgets.QHBoxLayout()
        self._main_layer.addWidget(self._vtk_frame, 4)
        self._main_layer.addWidget(self._panel_widget, 1)
        self.setLayout(self._main_layer)

        self._set_connections()

        self._storage_regist_key = "DiffFibrosis"

    def _set_connections(self):
        self._generate_button.clicked.connect(self.embed_uniform_point_distribution)
        self._update_button.clicked.connect(self.get_cube_arrays)

    def _initialize_uniform_points_widget(self):
        self._uniform_points_widget = QtWidgets.QWidget(self)
        self._uniform_points_layer = QtWidgets.QGridLayout()

        self._uniform_points_percent_label = QtWidgets.QLabel("Percent: ", self)
        self._uniform_points_percent_edit = QtWidgets.QLineEdit(self)
        self._uniform_points_percent_edit.setAlignment(QtCore.Qt.AlignCenter)
        self._uniform_points_percent_edit.setText("0")

        self._uniform_points_layer.addWidget(self._uniform_points_percent_label, 0, 0)
        self._uniform_points_layer.addWidget(self._uniform_points_percent_edit)

        self._uniform_points_widget.setLayout(self._uniform_points_layer)

    def _initialize_uniform_twigs_widget(self):
        self._uniform_twigs_widget = QtWidgets.QWidget(self)
        self._uniform_twigs_layer = QtWidgets.QGridLayout()

        self._uniform_twigs_percent_label = QtWidgets.QLabel("Percent", self)
        self._uniform_twigs_percent_edit = QtWidgets.QLineEdit(self)
        self._uniform_twigs_length_label = QtWidgets.QLabel("Length", self)
        self._uniform_twigs_length_edit = QtWidgets.QLineEdit(self)

        self._uniform_twigs_layer.addWidget(self._uniform_twigs_percent_label, 0, 0)
        self._uniform_twigs_layer.addWidget(self._uniform_twigs_percent_edit, 0, 1)
        self._uniform_twigs_layer.addWidget(self._uniform_twigs_length_label, 1, 0)
        self._uniform_twigs_layer.addWidget(self._uniform_twigs_length_edit, 1, 1)

        self._uniform_twigs_widget.setLayout(self._uniform_twigs_layer)

    def _initialize_distribution_box(self):
        self._distribution_box = QtWidgets.QGroupBox("Fibrosis distribution", self)

        self._distribution_combobox = QtWidgets.QComboBox(self)
        self._distribution_combobox.addItem("Uniform Points")
        self._distribution_stack = QtWidgets.QStackedWidget(self)
        self._distribution_stack.addWidget(self._uniform_points_widget)
        self._distribution_stack.addWidget(self._uniform_twigs_widget)

        self._distribution_layer = QtWidgets.QGridLayout()
        self._distribution_layer.addWidget(self._distribution_combobox, 0, 0, 1, 2)
        self._distribution_layer.addWidget(self._distribution_stack, 1, 0, 3, 2)

        self._distribution_box.setLayout(self._distribution_layer)

    def _initialize_control_box(self):
        self._control_box = QtWidgets.QGroupBox(self)

        self._update_button = QtWidgets.QPushButton("Update", self)
        self._upload_button = QtWidgets.QPushButton("Upload", self)
        self._generate_button = QtWidgets.QPushButton("Generate", self)
        self._export_button = QtWidgets.QPushButton("Export", self)

        self._control_layer = QtWidgets.QGridLayout()
        self._control_layer.addWidget(self._update_button, 0, 0)
        self._control_layer.addWidget(self._upload_button, 0, 1)
        self._control_layer.addWidget(self._generate_button, 1, 0)
        self._control_layer.addWidget(self._export_button, 1, 1)

        self._control_box.setLayout(self._control_layer)

    def _initialize_panel_widget(self):
        self._panel_widget = QtWidgets.QWidget(self)
        self._panel_layer = QtWidgets.QVBoxLayout()
        self._panel_layer.addWidget(self._distribution_box)
        self._panel_layer.addWidget(self._control_box)
        self._panel_layer.addStretch(5)

        self._panel_widget.setLayout(self._panel_layer)

    def _initialize_vtk_scene_widget(self):
        self._vtk_frame = QtWidgets.QFrame()

        vtk_scene = VtkDiffFibrosisScene(self._vtk_frame)

        self._vtk_layer = QtWidgets.QVBoxLayout()
        self._vtk_layer.addWidget(vtk_scene)
        self._vtk_frame.setLayout(self._vtk_layer)

        self._engine_manager = DiffFibrosisEngineManager()
        self._engine_manager.connect_with_scene(vtk_scene)

    def connect_with_storage(self, local_storage):
        self._local_storage = local_storage

    def start_vtk_scene(self):
        self._engine_manager.run_the_scene()

    def embed_uniform_point_distribution(self):
        self._engine_manager.embed_uniform_points_fibrosis(float(self._uniform_points_percent_edit.text()))

    def get_cube_arrays(self):
        data_dict = self._local_storage.get_access(self._storage_regist_key)
        self._engine_manager.set_data_dict(data_dict)
