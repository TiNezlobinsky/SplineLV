from PyQt5 import QtWidgets, QtCore

from LVSplineReconstruction.recon_engine_manager import ReconEngineManager
from LVSplineReconstruction.engine.vtk_reconstruction_scene import VtkReconstructionScene
from LVSplineReconstruction.widgets.display_box_widget import DisplayBoxWidget
from LVSplineReconstruction.widgets.reconstruction_main_menu_widget import ReconstructionMainMenuWidget
from LVSplineReconstruction.widgets.var_z_parameters_box import VarZParametersBox


# CODE REGIONS:
# 1) Widgets constructors
# 2) Initialization methods
# 3) SLOTS
# 3) SETTERS


class ReconstructionWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)

        self._engine_manager = None

        self._storage_regist_key = "Reconstruction"

        self._initialize_info_line()
        self._initialize_vtk_scene_widget()
        self._initialize_meridians_load_box()
        self._initialize_reconstruction_box()
        self._initialize_display_box()
        self._initialize_panel()

        self._main_layer = QtWidgets.QHBoxLayout()
        self._main_layer.addWidget(self._vtk_frame, 5)
        self._main_layer.addLayout(self._panel_layer, 1)

        self.setLayout(self._main_layer)

        self._set_connections()

# WIDGETS CONSTRUCTORS:

    def _set_connections(self):
        self._reconstruction_main_menu_widget.callUpdate.connect(self.update_storage_list)
        self._reconstruction_main_menu_widget.callUpload.connect(self.upload)
        self._reconstruction_main_menu_widget.callConstructDiffMesh.connect(self.construct_diff_mesh)
        self._reconstruction_main_menu_widget.callConstructPolySurface.connect(self.construct_poly_surface)
        self._display_box_widget.callSetOpacity.connect(self.set_opacity_value)
        self._display_box_widget.callSetVisualObject.connect(self.set_visual_object)

    def _initialize_meridians_load_box(self):
        self._reconstruction_main_menu_box = QtWidgets.QGroupBox("Meridians List", self)
        self._reconstruction_main_menu_widget = ReconstructionMainMenuWidget(self)
        self._reconstruction_main_menu_layer = QtWidgets.QHBoxLayout()
        self._reconstruction_main_menu_layer.addWidget(self._reconstruction_main_menu_widget)
        self._reconstruction_main_menu_box.setLayout(self._reconstruction_main_menu_layer)

    def _initialize_reconstruction_box(self):
        # union of mesh box and fibers box
        self._reconstruction_parameters_box = QtWidgets.QGroupBox("Reconstruction", self)
        self._var_z_parameters_box_widget = VarZParametersBox(self)
        self._reconstruction_layer = QtWidgets.QVBoxLayout()
        self._reconstruction_layer.addWidget(self._var_z_parameters_box_widget)
        self._reconstruction_parameters_box.setLayout(self._reconstruction_layer)

    def _initialize_display_box(self):
        self._display_box = QtWidgets.QGroupBox("Display", self)
        self._display_box_widget = DisplayBoxWidget(self)
        self._display_layer = QtWidgets.QGridLayout()
        self._display_layer.addWidget(self._display_box_widget)
        self._display_box.setLayout(self._display_layer)

    def _initialize_panel(self):
        self._panel_layer = QtWidgets.QGridLayout()
        self._panel_layer.addWidget(self._reconstruction_main_menu_box, 0, 0, 1, 2)
        self._panel_layer.addWidget(self._reconstruction_parameters_box, 1, 0, 1, 2)
        self._panel_layer.addWidget(self._display_box, 2, 0, 1, 2)

    def _initialize_vtk_scene_widget(self):
        self._vtk_frame = QtWidgets.QFrame()

        vtk_scene = VtkReconstructionScene(self._vtk_frame)

        self._vtk_layer = QtWidgets.QVBoxLayout()
        self._vtk_layer.addWidget(vtk_scene)
        self._vtk_layer.addWidget(self._info_line)
        self._vtk_frame.setLayout(self._vtk_layer)

        self._engine_manager = ReconEngineManager()
        self._engine_manager.connect_with_scene(vtk_scene)

    def _initialize_info_line(self):
        self._info_line = QtWidgets.QLineEdit(self)
        self._info_line.setReadOnly(True)

# INITIALIZATION METHODS:

    def start_vtk_scene(self):
        self._engine_manager.run_the_scene()

    def connect_with_storage(self, local_storage):
        self._local_storage = local_storage

# INFO LINE TEXT SET:

    def set_info_status(self, text):
        """
        Update the state of the info line when is needed
        Parameters
        ----------
        text : str
            Text to be displayed
        """
        self._info_line.setText(text)

# SLOTS:
# As a reaction on a user actions (push buttons, etc.)

    def update_storage_list(self):
        data_dict = self._local_storage.get_access(self._storage_regist_key)
        if not data_dict:
            # check if empty
            return
        self._engine_manager.set_data_dict(data_dict)
        self._reconstruction_main_menu_widget.set_meridians_list(len(data_dict["meridians"]))

    def upload(self):
        self._local_storage.upload_data(self._storage_regist_key,
                                        self._engine_manager.get_reconstructed())

    def construct_diff_mesh(self):
        self.set_reconstruction_parameters()
        self.set_fibers_field_parameters()
        self._engine_manager.construct_mesh()
        self._engine_manager.visualize_diff_mesh()

    def construct_poly_surface(self):
        self.set_reconstruction_parameters()
        self.set_fibers_field_parameters()
        self._engine_manager.construct_polygonal_surfaces()
        self._engine_manager.visualize_elem_surface()

    def export_diff_mesh(self):
        self._engine_manager.write_unstructured_grid()

    def export_poly_surface(self):
        self._engine_manager.write_polydata_grid()

    def set_opacity_value(self, i):
        self._engine_manager.set_opacity(i / 100.)  # should be float

    def set_visual_object(self, text):
        if text == 0: # "FiniteDiffMesh"
            self._engine_manager.visualize_diff_mesh()
        elif text == 1: # "FiniteElemSurface"
            self._engine_manager.visualize_elem_surface()
        elif text == 2: # "FibersField"
            self._engine_manager.visualize_fibers()

# SETTERS:

    def set_reconstruction_parameters(self):
        self._engine_manager.set_wall_points(self._var_z_parameters_box_widget.get_wall_points())
        self._engine_manager.set_surface_points(self._var_z_parameters_box_widget.get_surface_points())
        self._engine_manager.set_layers_number(self._var_z_parameters_box_widget.get_layers_number())

    def set_fibers_field_parameters(self):
        self._engine_manager.set_gamma_0(self._var_z_parameters_box_widget.get_gamma_0())
        self._engine_manager.set_gamma_1(self._var_z_parameters_box_widget.get_gamma_1())
