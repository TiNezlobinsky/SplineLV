from PyQt5 import QtWidgets, QtCore

from SplineMeasurement.meas_engine_manager import MeasEngineManager
from SplineMeasurement.engine.vtk_meas_scene import VtkMeasScene
from SplineMeasurement.widgets.gui_median_widget import GuiMedianWidget
from SplineMeasurement.widgets.image_widgets.image_geometry_widget import ImageGeometryWidget
from SplineMeasurement.widgets.image_widgets.positioning_widget import PositioningWidget
from SplineMeasurement.widgets.mesh_widgets.mesh_geometry_widget import MeshGeometryWidget
from SplineMeasurement.widgets.mesh_widgets.transform_widget import TransformWidget
from SplineMeasurement.widgets.data_control_widget import DataControlWidget


# CODE REGIONS:
# 1) Initialization
# 2) Objects list management
# 3) Local storage management
# 4) Meridian splines management


class MeasurementWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)

        self._initialize_info_line()
        self._initialize_vtk_scene_widget()
        self._initialize_engine_manager()

        # gui widgets initialization:
        self._initialize_list_box()
        self._initialize_image_tabs()
        self._initialize_mesh_tabs()
        self._initialize_stack_widget()
        self._initialize_gui_median_widget()
        self._initialize_panel()

        self._main_layer = QtWidgets.QHBoxLayout()
        self._main_layer.addWidget(self._vtk_frame, 4)
        self._main_layer.addLayout(self._panel_layer, 1)

        self.setLayout(self._main_layer)

        self._storage_regist_key = "VarBaseMeasurement"

        self._set_connections()

    def _set_connections(self):
        self._data_control_widget.callLoad.connect(self.load)
        self._data_control_widget.callSwitchRow.connect(self.switch_row)
        self._data_control_widget.callUpload.connect(self.upload)
        self._gui_median_widget.callSwitchLeftEndoInteraction.connect(self.switch_left_endo_interaction_mode)
        self._gui_median_widget.callSwitchRightEndoInteraction.connect(self.switch_right_endo_interaction_mode)
        self._gui_median_widget.callSwitchLeftEpiInteraction.connect(self.switch_left_epi_interaction_mode)
        self._gui_median_widget.callSwitchRightEpiInteraction.connect(self.switch_right_epi_interaction_mode)
        self._gui_median_widget.callLeftMeridian.connect(self.call_left_meridian)
        self._gui_median_widget.callRightMeridian.connect(self.call_right_meridian)
        self._gui_median_widget.callResetLeftMeridian.connect(self.reset_left_meridian)
        self._gui_median_widget.callResetRightMeridian.connect(self.reset_right_meridian)

# INITIALIZATION:

    def _initialize_vtk_scene_widget(self):
        self._vtk_frame = QtWidgets.QFrame()
        self._vtk_scene = VtkMeasScene(self._vtk_frame)
        self._vtk_layer = QtWidgets.QVBoxLayout()

        self._vtk_layer.addWidget(self._vtk_scene)
        self._vtk_layer.addWidget(self._info_line)
        self._vtk_frame.setLayout(self._vtk_layer)

    def _initialize_info_line(self):
        self._info_line = QtWidgets.QLineEdit(self)
        self._info_line.setReadOnly(True)

    def _initialize_engine_manager(self):
        self._engine_manager = MeasEngineManager()
        self._engine_manager.connect_with_scene(self._vtk_scene)

    def _initialize_list_box(self):
        self._data_control_box = QtWidgets.QGroupBox("Slice list")
        self._data_control_widget = DataControlWidget(self)
        self._data_control_widget.connect_with_engine_manager(self._engine_manager)
        self._data_control_layer = QtWidgets.QHBoxLayout()
        self._data_control_layer.addWidget(self._data_control_widget)
        self._data_control_box.setLayout(self._data_control_layer)

    def _initialize_image_tabs(self):
        self._initialize_positioning_widget()
        self._initialize_image_geometry_widget()
        self._image_tab_widget = QtWidgets.QTabWidget(self)
        self._image_tab_widget.addTab(self._positioning_widget, "Positioning")
        self._image_tab_widget.addTab(self._image_geometry_widget, "Geometry")

    def _initialize_positioning_widget(self):
        self._positioning_widget = PositioningWidget(self)
        self._positioning_widget.connect_with_engine_manager(self._engine_manager)

    def _initialize_image_geometry_widget(self):
        self._image_geometry_widget = ImageGeometryWidget(self)
        self._image_geometry_widget.connect_with_engine_manager(self._engine_manager)

    def _initialize_mesh_tabs(self):
        self._initialize_transform_widget()
        self._initialize_mesh_geometry_widget()
        self._mesh_tab_widget = QtWidgets.QTabWidget(self)
        self._mesh_tab_widget.addTab(self._transform_widget, "Transform")
        self._mesh_tab_widget.addTab(self._mesh_geometry_widget, "Geometry")

    def _initialize_transform_widget(self):
        self._transform_widget = TransformWidget(self)
        self._transform_widget.connect_with_engine_manager(self._engine_manager)

    def _initialize_mesh_geometry_widget(self):
        self._mesh_geometry_widget = MeshGeometryWidget(self)
        self._mesh_geometry_widget.connect_with_engine_manager(self._engine_manager)

    def _initialize_stack_widget(self):
        self._stack_widget = QtWidgets.QStackedWidget(self)
        self._stack_widget.insertWidget(0, self._image_tab_widget)
        self._stack_widget.insertWidget(1, self._mesh_tab_widget)
        self._stack_widget.hide()

    def _initialize_gui_median_widget(self):
        self._gui_median_widget = GuiMedianWidget(self)
        self._gui_median_widget.connect_with_engine_manager(self._engine_manager)

    def _initialize_panel(self):
        self._panel_layer = QtWidgets.QVBoxLayout()
        self._panel_layer.addWidget(self._data_control_box)
        self._panel_layer.addWidget(self._stack_widget)
        self._panel_layer.addWidget(self._gui_median_widget)

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

# OBJECTS LIST MANAGEMENT:

    def start_vtk_scene(self):
        """
        Run the scene. Should be called after the object initialization only
        """
        self._engine_manager.run_the_scene()
        self.set_info_status("Ready")

    def new_list_initialization(self, files_format):
        """
        Switches the tools according to files format (type)

        Parameters
        ----------
        files_format : str
        """

        if files_format == "image":
            self._stack_widget.setCurrentIndex(0)
            self.set_info_status("Data is loaded. Current tool type: image")
        elif files_format == "mesh":
            self._stack_widget.setCurrentIndex(1)
            self.set_info_status("Data is loaded. Current tool type: mesh")
        else:
            return
        self._stack_widget.show()

    def load(self):
        """
        Load the directory with target files (slices) and
        form objects list
        """
        folder_name = str(QtWidgets.QFileDialog.getExistingDirectory(self, "Open folder", './',
                                                                 QtWidgets.QFileDialog.ShowDirsOnly))

        if folder_name == '':
            return
        self._data_control_widget.set_text_to_load_line(folder_name)
        self._engine_manager.set_data_dir(folder_name)
        self._engine_manager.load_data()
        self._data_control_widget.add_rows_to_list_widget(self._engine_manager.get_file_name_list())

        self.new_list_initialization(self._engine_manager.get_files_format())

    def switch_row(self, row):
        """
        Switch the slice

        Parameters
        ----------
        row : int
            slice number
        """
        self._engine_manager.switch_scene(row)
        # self._change_widgets_state()

# LOCAL STORAGE MANAGEMENT:

    def upload(self):
        """
        Upload data to local storage with "VarBaseMeasurement" key.
        Data: spline coordinates (nodes) on each section.
        """
        self._engine_manager.save_meridians_dict()
        self._local_storage.upload_data(self._storage_regist_key,
                                        self._engine_manager.get_data_dict())
        self.set_info_status("Measurements were loaded to the local storage")

    def connect_with_storage(self, local_storage):
        """
        Connect with the local storage to exchange data between packages

        Parameters
        ----------
        local_storage : object
            LocalStorage class object
        """
        self._local_storage = local_storage
        self._local_storage.add_block(self._storage_regist_key)

# MERIDIAN SPLINES MANAGEMENT:

    def switch_left_endo_interaction_mode(self):
        if self._gui_median_widget.get_left_endo_mode():
            self._engine_manager.left_endo_interaction_off()
        else:
            self._engine_manager.left_endo_interaction_on()
            # print ("Endo left: ", self._gui_median_widget.get_left_endo_mode())
            # print ("Endo right: ", self._gui_median_widget.get_right_endo_mode())
            # print ("Epi left: ", self._gui_median_widget.get_left_endo_mode())
            # print ("Epi right: ", self._gui_median_widget.get_right_endo_mode())

    def switch_right_endo_interaction_mode(self):
        if self._gui_median_widget.get_right_endo_mode():
            self._engine_manager.right_endo_interaction_off()
        else:
            self._engine_manager.right_endo_interaction_on()

    def switch_left_epi_interaction_mode(self):
        if self._gui_median_widget.get_left_epi_mode():
            self._engine_manager.left_epi_interaction_off()
        else:
            self._engine_manager.left_epi_interaction_on()

    def switch_right_epi_interaction_mode(self):
        if self._gui_median_widget.get_right_epi_mode():
            self._engine_manager.right_epi_interaction_off()
        else:
            self._engine_manager.right_epi_interaction_on()

    def call_left_meridian(self):
        if self._gui_median_widget.get_left_meridian_state():
            self._engine_manager.activate_left_meridian()
        else:
            self._engine_manager.inactivate_left_meridian()

    def call_right_meridian(self):
        if self._gui_median_widget.get_right_meridian_state():
            self._engine_manager.activate_right_meridian()
        else:
            self._engine_manager.inactivate_right_meridian()

    def reset_right_meridian(self):
        self._engine_manager.reset_right_meridian()

    def reset_left_meridian(self):
        self._engine_manager.reset_left_meridian()

if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)

    measurement_widget = MeasurementWidget()

    main_window = QtWidgets.QMainWindow()
    main_window.setCentralWidget(measurement_widget)
    main_window.show()
    measurement_widget.start_vtk_scene()

    sys.exit(app.exec_())
