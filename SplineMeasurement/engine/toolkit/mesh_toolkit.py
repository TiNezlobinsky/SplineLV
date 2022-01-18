import vtk
from math import degrees, acos
from numpy.linalg import det
from numpy import matrix
from SplineMeasurement.engine.vtk_widgets.movable_lines import MovableLine


# CODE REGIONS:
# 1) Initialization
# 2) Setters
# 3) Getters
# 4) Scene updating
# 5) Apex thickness
# 6) Align slices XOY
# 7) Affine transformations
# 8) Static methods


class MeshToolkit:
    def __init__(self, vtk_scene):

        self._vtk_scene = vtk_scene

        self._current_slice = None
        self._current_renderer = None
        self._current_slice_number = 0

        self._meshes_list = []
        self._renderer_list = []
        self._apex_level_line = []

        self._h = 10.

        self._apex_level_line_state = False

# INITIALIZATION:

    def initialize_toolkit(self):
        for i in range(len(self._meshes_list)):
            self._meshes_list[i] = self._align_mesh(self._meshes_list[i])
            self._initialize_apex_level_lines(self._renderer_list[i])

        self._initialize_vtk_events()

    def _initialize_vtk_events(self):
        self._vtk_scene.AddObserver("LeftButtonPressEvent", self.vtk_observer_add_level_line)

    def _initialize_apex_level_lines(self, renderer):
        self._apex_level_line.append(MovableLine([0, 1, 1]))
        self._apex_level_line[-1].connect_with_renderer(renderer)

# SETTERS:

    def set_meshes_list(self, meshes_list):
        self._meshes_list = meshes_list

    def set_renderer_list(self, renderer_list):
        self._renderer_list = renderer_list

    def set_scene_elements_list(self, scene_elements_list):
        self._scene_elements_list = scene_elements_list

    def set_interactor(self, interactor):
        self._interactor = interactor

    def set_interator_style(self, interactor_style):
        self._interactor_style = interactor_style

    def set_current_slice_number(self, number):
        self._current_slice_number = number

    def set_vtk_scene(self, vtk_scene):
        self._vtk_scene = vtk_scene

    def set_mesh_apex_level_line_state(self, state):
        self._apex_level_line_state = state

# GETTERS:

    def get_h(self):
        return self._h

# SCENE UPDATING:

    def _set_references(self):
        # set references according to current image (slice) number
        self._current_slice = self._meshes_list[self._current_slice_number]
        self._current_renderer = self._renderer_list[self._current_slice_number]

    def update(self):
        self._set_references()

# APEX THICKNESS:

    def add_level_line(self):
        if self._apex_level_line_state:
            picked_position = list(self._interactor_style.get_picked_position())
            picked_position[0] = 0
            picked_position[2] = 0
            pos_y = picked_position[1]
            span = 12
            self._apex_level_line[self._current_slice_number].set_point_1([-span, pos_y, 0])
            self._apex_level_line[self._current_slice_number].set_point_2([span, pos_y, 0])
            self._h = pos_y
            self._interactor.Initialize()
        else:
            self._remove_level_line()

    def vtk_observer_add_level_line(self, obj, event):
        self.add_level_line()

    def _remove_level_line(self):
        if "_current_renderer" in self.__dict__:
            # self._current_renderer.RemoveActor(self._level_line_actor)
            self._interactor.Initialize()

# ALIGN SLICES XOY:

    def rotate(self, axis, angle_value):
        if axis == "x":
            self._current_slice = self._rotate_x(self._current_slice, angle_value)
            self._meshes_list[self._current_slice_number] = self._current_slice
        elif axis == "y":
            self._current_slice = self._rotate_y(self._current_slice, angle_value)
            self._meshes_list[self._current_slice_number] = self._current_slice
        elif axis == "z":
            self._current_slice = self._rotate_z(self._current_slice, angle_value)
            self._meshes_list[self._current_slice_number] = self._current_slice
        else:
            return

    def _align_mesh(self, slice_):
        res_slice = vtk.vtkUnstructuredGrid()
        res_slice.DeepCopy(slice_)
        res_slice = self._align_to_y(res_slice)
        angle_step = 0.5  # rotational step
        res_slice = self._align_to_x(res_slice, angle_step)
        return res_slice

    def _align_to_y(self, res_slice):
        vector_x = [1, 0, 0]
        vector_y = [0, 1, 0]
        camera_vector = [0, 0, -1]

        rotate_angle = acos(vtk.vtkMath.Dot(vector_y, camera_vector))

        rotate_angle = degrees(rotate_angle)

        tr_prod = self._triple_product(vector_y, camera_vector, vector_x)

        if tr_prod < 0:
            rotate_angle = -rotate_angle
        res_slice = self._rotate_x(res_slice, rotate_angle)

        return res_slice

    def _align_to_x(self, res_slice, angle_step):
        # without rotation control
        # there may be a problem with right-left orientation
        angle_step = abs(angle_step)
        sum_angle = 0.  # to control rotational angle value

        bound_range_z = self._get_bound_range_z(res_slice)
        while bound_range_z > 5.:
            res_slice = self._rotate_y(res_slice, angle_step)
            bound_range_z = self._get_bound_range_z(res_slice)
            sum_angle += angle_step

        if angle_step > 90:
            res_slice = self._rotate_y(res_slice, 90)

        return res_slice

# AFFINE TRANSFORMATION:

    def _rotate_transform(self, transform, slice_):
        transfilter = vtk.vtkTransformFilter()
        transfilter.SetInputData(slice_)
        transfilter.SetTransform(transform)
        transfilter.Update()
        return transfilter.GetOutput()

    def _rotate_x(self, slice_, rotate_angle):
        transform = vtk.vtkTransform()
        transform.RotateX(rotate_angle)
        return self._rotate_transform(transform, slice_)

    def _rotate_y(self, slice_, rotate_angle):
        transform = vtk.vtkTransform()
        transform.RotateY(rotate_angle)
        return self._rotate_transform(transform, slice_)

    def _rotate_z(self, slice_, rotate_angle):
        transform = vtk.vtkTransform()
        transform.RotateZ(rotate_angle)
        return self._rotate_transform(transform, slice_)

# STATIC METHODS:

    @staticmethod
    def _get_bound_range_z(slice_):
        bounds_array = slice_.GetBounds()
        range_z = bounds_array[5] - bounds_array[4]
        return range_z

    @staticmethod
    def _triple_product(vector_1, vector_2, vector_3):
        matrix_ = matrix([vector_1, vector_2, vector_3])
        determine = det(matrix_)
        return determine
