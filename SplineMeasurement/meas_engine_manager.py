import os
import vtk
from SplineMeasurement.engine.vtk_widgets.meridian_spline_widget import MeridianSplineWidget
from SplineMeasurement.engine.toolkit.ultrasound_toolkit import UltrasoundToolkit
from SplineMeasurement.engine.toolkit.mesh_toolkit import MeshToolkit

from SplineMeasurement.additions.decorators import check_initialization


# CODE REGIONS:
# 1) Initialization
# 2) Scene management
# 3) Getters
# 4) Setters
# 5) Files reading
# 6) Saving data to export
# 7) Image actions
# 8) Mesh actions
# 9) Spline control through the meridian widgets


class MeasEngineManager:
    """
    Central class for the package controlling.
    Binds with MeasurementWidget to provide it's methods
    for application management
    """
    # use check_initialization decorator to activate method after the
    # objects (slices) loading
    def __init__(self):

        self._data_dir = None

        self._toolkit = None

        self._vtk_scene = None

        self._files_format = ""

# INITIALIZATION:

    def _initialize_structures(self):
        self._current_slice_number = 0

        self._objects_count = 0  # same as len(self._objects_list)

        self._files_name_list = []

        self._objects_list = []
        self._original_objects_list = []

        self._data_dict = {}

        self._left_meridian_spline_widgets_list = []
        self._right_meridian_spline_widgets_list = []

        self._vtk_widgets_state_dict = {"left_meridian": False,
                                        "right_meridian": False}

    def _scene_initialization(self, files):
        self._initialize_structures()
        for file_ in files:
            full_path = os.path.join(self._data_dir, file_)
            output = self.open_file(full_path)
            if output:
                self._objects_list.append(output)
                self._original_objects_list.append(self.open_file(full_path))  # make a copy with vtk ?
                self._files_name_list.append(file_)
                self._objects_count += 1
            else:
                continue

        self._vtk_scene.set_files_type(self._files_format)
        self._vtk_scene.set_objects_list(self._objects_list)
        self._vtk_scene.set_objects_count(self._objects_count)

        self._vtk_scene.initialize_scene()
        self._initialize_toolkit()
        self._initialize_meridian_spline_widgets()

    def _initialize_meridian_spline_widgets(self):
        for i in range(self._objects_count):
            self._left_meridian_spline_widgets_list.append(MeridianSplineWidget("left", [0.5, 0.5, 1], [1, 0.2, 0.6]))
            self._left_meridian_spline_widgets_list[i].set_renderer(self._vtk_scene.get_renderer(i))
            self._left_meridian_spline_widgets_list[i].set_interactor(self._vtk_scene.get_interactor())
            self._left_meridian_spline_widgets_list[i].set_Z(100.)  # default Z
            self._left_meridian_spline_widgets_list[i].set_h(8.)  # default h
            self._left_meridian_spline_widgets_list[i].set_vtk_scene(self._vtk_scene)
            self._left_meridian_spline_widgets_list[i].initialize_splines()

            self._right_meridian_spline_widgets_list.append(MeridianSplineWidget("right", [0, 1.0, 0], [1, 0.8, 0.1]))
            self._right_meridian_spline_widgets_list[i].set_renderer(self._vtk_scene.get_renderer(i))
            self._right_meridian_spline_widgets_list[i].set_interactor(self._vtk_scene.get_interactor())
            self._right_meridian_spline_widgets_list[i].set_Z(100.)
            self._right_meridian_spline_widgets_list[i].set_h(8.)
            self._right_meridian_spline_widgets_list[i].set_vtk_scene(self._vtk_scene)
            self._right_meridian_spline_widgets_list[i].initialize_splines()

    def _initialize_toolkit(self):
        if self._files_format == "image":
            self._toolkit = UltrasoundToolkit(self._vtk_scene)
            self._toolkit.set_interactor(self._vtk_scene.get_interactor())
            self._toolkit.set_interator_style(self._vtk_scene.get_interactor_style())
            self._toolkit.set_images_list(self._objects_list)
            self._toolkit.set_renderer_list(self._vtk_scene.get_renderer_list())
        elif self._files_format == "mesh":
            self._toolkit = MeshToolkit(self._vtk_scene)
            self._toolkit.set_interactor(self._vtk_scene.get_interactor())
            self._toolkit.set_interator_style(self._vtk_scene.get_interactor_style())
            self._toolkit.set_meshes_list(self._objects_list)
            self._toolkit.set_renderer_list(self._vtk_scene.get_renderer_list())
            self._toolkit.set_scene_elements_list(self._vtk_scene.get_scene_elements_list())
        else:
            # send signal
            return
        self._toolkit.initialize_toolkit()

    def load_data(self):
        """
        Initialize the vtk scene with selected objects (slices)
        """
        # problems with an understanding how the destructors for the vtk object
        # through the python references are works.
        # this is a fast fix to prevent old splines appearance after reloading:
        self.inactivate_left_meridian()
        self.inactivate_right_meridian()
        # end

        files = os.listdir(self._data_dir)
        self._scene_initialization(files)

# SCENE MANAGEMENT:

    def connect_with_scene(self, vtk_scene):
        """
        Connect with the scene

        Parameters
        ----------
        vtk_scene : vtk object
            VtkScene class object
        """
        self._vtk_scene = vtk_scene

    def run_the_scene(self):
        """
        Run the scene. Initialize vtk window
        """
        self._vtk_scene.initialize_window()

    def switch_scene(self, i):
        """
        Switch current object on the scene to manipulate

        Parameters
        ----------
        i : int
            slice (object) number
        """
        self._inactivate_splines()
        self._vtk_scene.set_current_scene_frame(i)
        self._toolkit.set_current_slice_number(i)
        self._toolkit.update()
        self._current_slice_number = i
        self._change_state()

# GETTERS:

    def get_vtk_scene(self):
        """
        Get the vtk scene, which was connected

        Returns
        -------
        get_vtk_scene : VtkMeasScene object
        """
        return self._vtk_scene

    def get_file_name_list(self):
        """
        Get the files name list

        Returns
        -------
        get_file_name_list : list
        """
        return self._files_name_list

    def get_files_format(self):
        """
        Get the files format (current objects type)

        Returns
        -------
        get_files_format : str
        """
        return self._files_format

    def get_data_dict(self):
        """
        Get the data dict with the measured slices (splines nodes)

        Returns
        -------
        get_data_dict : dict
        """
        # self._data_dict attribute appears after the first loading
        try:
            return self._data_dict
        except AttributeError:
            pass

# SETTERS:

    # def set_current_slice_number(self):
    #     self._current_slice_number = self._vtk_scene.get_current_slice_number()

    def set_data_dir(self, dir_):
        """
        Set the files (objects) directory name

        Parameters
        ----------
        dir_ : str
        """
        self._data_dir = dir_

# FILES READING:

    def open_file(self, file_name):
        """
        Open the file with a slice

        Parameters
        ----------
        file_name : str
            should contains the extension to define a file type

        Returns
        -------
        open_file : vtk object or False
            vtk reader for the appropriate type (image, mesh, ...)
        """
        if ".jpeg" in file_name or ".jpg" in file_name:
            return self._open_jpeg(file_name)
        elif ".png" in file_name:
            return self._open_png(file_name)
        elif ".bmp" in file_name:
            return self._open_bmp(file_name)
        elif ".dcm" in file_name:
            return self._open_dicom(file_name)
        elif ".vtk" in file_name:
            return self._open_vtk(file_name)
        else:
            return False

    def _open_jpeg(self, file_name):
        reader = vtk.vtkJPEGReader()
        reader.SetFileName(file_name)
        reader.Update()
        self._files_format = "image"
        return reader.GetOutput()

    def _open_png(self, file_name):
        reader = vtk.vtkPNGReader()
        reader.SetFileName(file_name)
        reader.Update()
        self._files_format = "image"
        return reader.GetOutput()

    def _open_bmp(self, file_name):
        reader = vtk.vtkBMPReader()
        reader.SetFileName(file_name)
        reader.Update()
        self._files_format = "image"
        return reader.GetOutput()

    def _open_dicom(self, file_name):
        reader = vtk.vtkDICOMImageReader()
        reader.SetFileName(file_name)
        reader.Update()
        self._files_format = "image"
        return reader.GetOutput()

    def _open_vtk(self, file_name):
        reader = vtk.vtkUnstructuredGridReader()
        reader.SetFileName(file_name)
        reader.Update()
        self._files_format = "mesh"
        return reader.GetOutput()

# SAVING DATA TO EXPORT:

    @check_initialization
    def save_meridians_dict(self):
        """
        Pack the measurement results (spline nodes on each slice) to use in other packages
        """
        # Need try - except block here
        if self._files_format == "image":
            scale_coeff = self._toolkit.get_scale_coeff()*10  # mm
        else:
            scale_coeff = 1

        # usually should be two meridians in each object (image or mesh):
        self._data_dict["meridians"] = [0]*self._objects_count*2
        # common to all meridians:
        self._data_dict["common"] = {"h": self._toolkit.get_h()*scale_coeff}

        for i in range(self._objects_count):
            self._data_dict["meridians"][i] = {}
            # add first meridian:
            self._data_dict["meridians"][i]["epi"] = {
                "ro": list(self._left_meridian_spline_widgets_list[i].get_epi_ro_coordinates()*scale_coeff),
                "z": list(self._left_meridian_spline_widgets_list[i].get_epi_z_coordinates()*scale_coeff),
                "Zmax": self._left_meridian_spline_widgets_list[i].get_Z()*scale_coeff # same as in "endo"
            }

            self._data_dict["meridians"][i]["endo"] = {
                "ro": list(self._left_meridian_spline_widgets_list[i].get_endo_ro_coordinates()*scale_coeff),
                "z": list(self._left_meridian_spline_widgets_list[i].get_endo_z_coordinates()*scale_coeff),
                "Zmax": self._left_meridian_spline_widgets_list[i].get_Z()*scale_coeff  # same as in "epi"
            }

            self._data_dict["meridians"][self._objects_count + i] = {}
            # add second (opposite) meridian:
            self._data_dict["meridians"][self._objects_count + i]["epi"] = {
                "ro": list(self._right_meridian_spline_widgets_list[i].get_epi_ro_coordinates()*scale_coeff),
                "z": list(self._right_meridian_spline_widgets_list[i].get_epi_z_coordinates()*scale_coeff),
                "Zmax": self._right_meridian_spline_widgets_list[i].get_Z()*scale_coeff  # same as in "endo"
            }
            self._data_dict["meridians"][self._objects_count + i]["endo"] = {
                "ro": list(self._right_meridian_spline_widgets_list[i].get_endo_ro_coordinates()*scale_coeff),
                "z": list(self._right_meridian_spline_widgets_list[i].get_endo_z_coordinates()*scale_coeff),
                "Zmax": self._right_meridian_spline_widgets_list[i].get_Z()*scale_coeff  # same as in "epi"
            }


# IMAGE ACTIONS (ultrasound toolkit):

    @check_initialization
    def set_marking_state(self, state):
        self._toolkit.set_marking_state(state)

    @check_initialization
    def set_label_lines_visibility_state(self, state):
        self._label_lines_visibility_state = state

    @check_initialization
    def set_ruler_state(self, state):
        self._toolkit.set_ruler_state(state)

    @check_initialization
    def set_cm_number(self, number):
        self._toolkit.set_cm_number(number)

    @check_initialization
    def calculate_scale_coeff(self):
        self._toolkit.calculate_scale_coeff()

    @check_initialization
    def set_image_apex_level_line_state(self, state):
        self._toolkit.set_apex_level_line_state(state)

    @check_initialization
    def set_h(self):
        h = self._toolkit.get_h()
        for i in range(self._objects_count):
            self._left_meridian_spline_widgets_list[i].update_h(h)
            self._right_meridian_spline_widgets_list[i].update_h(h)

    def get_h(self):
        return self._toolkit.get_h()

    def get_label_lines_visibility_state(self):
        return self._label_lines_visibility_state

    def get_scaled_h(self):
        return self._toolkit.get_scaled_h()

    @check_initialization
    def rotate_image_to_axis(self):
        self._toolkit.rotate_image_to_axis()
        self._toolkit.update()
        self._vtk_scene.set_object(self._current_slice_number, self._toolkit.get_object())

    @check_initialization
    def remove_marks(self):
        self._toolkit.remove_marks()

# MESH ACTIONS (mesh toolkit):

    @check_initialization
    def rotate_x(self, angle_value):
        self._toolkit.rotate("x", angle_value)

    @check_initialization
    def rotate_y(self, angle_value):
        self._toolkit.rotate("y", angle_value)

    @check_initialization
    def rotate_z(self, angle_value):
        self._toolkit.rotate("z", angle_value)

    @check_initialization
    def set_mesh_apex_level_line_state(self, state):
        self._toolkit.set_mesh_apex_level_line_state(state)

# SPLINE CONTROL THROUGH THE MERIDIAN WIDGETS:

    def _inactivate_splines(self):
        # to prevent conflicts between active splines
        self._left_meridian_spline_widgets_list[self._current_slice_number].inactivate()
        self._right_meridian_spline_widgets_list[self._current_slice_number].inactivate()


    def _change_state(self):
        if self._vtk_widgets_state_dict["left_meridian"]:
            self._left_meridian_spline_widgets_list[self._current_slice_number].activate()
        else:
            self._left_meridian_spline_widgets_list[self._current_slice_number].inactivate()

        if self._vtk_widgets_state_dict["right_meridian"]:
            self._right_meridian_spline_widgets_list[self._current_slice_number].activate()
        else:
            self._right_meridian_spline_widgets_list[self._current_slice_number].inactivate()

    @check_initialization
    def left_epi_interaction_on(self):
        self._left_meridian_spline_widgets_list[self._current_slice_number].epi_spline_interaction_on()

    @check_initialization
    def left_epi_interaction_off(self):
        self._left_meridian_spline_widgets_list[self._current_slice_number].epi_spline_interaction_off()

    @check_initialization
    def left_endo_interaction_on(self):
        self._left_meridian_spline_widgets_list[self._current_slice_number].endo_spline_interaction_on()

    @check_initialization
    def left_endo_interaction_off(self):
        self._left_meridian_spline_widgets_list[self._current_slice_number].endo_spline_interaction_off()

    @check_initialization
    def right_epi_interaction_on(self):
        self._right_meridian_spline_widgets_list[self._current_slice_number].epi_spline_interaction_on()

    @check_initialization
    def right_epi_interaction_off(self):
        self._right_meridian_spline_widgets_list[self._current_slice_number].epi_spline_interaction_off()

    @check_initialization
    def right_endo_interaction_on(self):
        self._right_meridian_spline_widgets_list[self._current_slice_number].endo_spline_interaction_on()

    @check_initialization
    def right_endo_interaction_off(self):
        self._right_meridian_spline_widgets_list[self._current_slice_number].endo_spline_interaction_off()

    @check_initialization
    def activate_left_meridian(self):
        self._left_meridian_spline_widgets_list[self._current_slice_number].activate()
        self._vtk_widgets_state_dict["left_meridian"] = True

    @check_initialization
    def activate_right_meridian(self):
        self._right_meridian_spline_widgets_list[self._current_slice_number].activate()
        self._vtk_widgets_state_dict["right_meridian"] = True

    @check_initialization
    def inactivate_left_meridian(self):
        self._left_meridian_spline_widgets_list[self._current_slice_number].inactivate()
        self._vtk_widgets_state_dict["left_meridian"] = False

    @check_initialization
    def inactivate_right_meridian(self):
        self._right_meridian_spline_widgets_list[self._current_slice_number].inactivate()
        self._vtk_widgets_state_dict["right_meridian"] = False

    @check_initialization
    def reset_right_meridian(self):
        self._right_meridian_spline_widgets_list[self._current_slice_number].reset()

    @check_initialization
    def reset_left_meridian(self):
        self._left_meridian_spline_widgets_list[self._current_slice_number].reset()
