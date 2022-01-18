import vtk
from math import degrees, sqrt
from numpy.linalg import det
from numpy import matrix
from SplineMeasurement.engine.vtk_widgets.movable_lines import MovableLine
from SplineMeasurement.engine.vtk_widgets.backlight_handle_widget import BacklightHandleWidget


# CODE REGIONS:
# 1) Initialization
# 2) Setters
# 3) Getters
# 4) Scene updating
# 5) Baclight handles
# 6) Ruler
# 7) Label lines
# 8) Marking
# 9) Apex thickness
# 10) Change of coordinate system
# 11) Static methods


class UltrasoundToolkit:
    def __init__(self, vtk_scene):

        self._vtk_scene = vtk_scene

        self._current_slice = None
        self._current_renderer = None
        self._current_slice_number = 0

        self._images_list = []
        self._renderer_list = []
        self._spin_axis_list = []
        self._base_lines_list = []
        self._apex_level_line = []
        self._image_extent_list = []
        self._camera_rotation_list = []

        self._h = 10.              # apex thickness in Cartesian coordinates
        self._scaled_h = 10.       # apex thickness in cm (average)
        self._scaled_h_list = []   # contains apex thickness in cm for each slice
        self._cm_number = 1
        self._scale_coeff = 1.
        self._scale_coeff_list = []

        self._marking_state = False
        self._apex_level_line_state = False
        self._label_lines_visibility_state = False
        self._ruler_state = False

# INITIALIZATION:

    def initialize_toolkit(self):
        for i in range(len(self._images_list)):
            self._image_extent_list.append(self._get_image_extent(self._images_list[i]))
            self._initialize_label_lines(self._renderer_list[i])
            self._spin_axis_list[-1].get_actor().GetProperty().SetOpacity(1.)
            self._base_lines_list[-1].get_actor().GetProperty().SetOpacity(1.)
            self._camera_rotation_list.append(0)  # angle value (degrees)
            self._scaled_h_list.append(0.)
            self._scale_coeff_list.append(0)

        self._initialize_backlight_handles()
        self._initialize_ruler()
        self._initialize_vtk_events()

    def _initialize_vtk_events(self):
        self._vtk_scene.AddObserver("LeftButtonPressEvent", self.vtk_observer_marking)
        self._vtk_scene.AddObserver("LeftButtonPressEvent", self.vtk_observer_add_level_line)
        self._vtk_scene.AddObserver("LeftButtonPressEvent", self._vtk_observer_call_ruler)

# SETTERS:

    def set_vtk_scene(self, vtk_scene):
        self._vtk_scene = vtk_scene

    def set_images_list(self, images_list):
        self._images_list = images_list

    def set_renderer_list(self, renderer_list):
        self._renderer_list = renderer_list

    def set_interactor(self, interactor):
        self._interactor = interactor

    def set_interator_style(self, interactor_style):
        self._interactor_style = interactor_style

    def set_current_slice_number(self, number):
        self._current_slice_number = number

    def set_h(self, h):
        self._scaled_h_list[self._current_slice_number] = h*self._scale_coeff
        self._scaled_h = self.list_average(self._scaled_h_list)
        self._h = h

    def set_marking_state(self, state):
        self._marking_state = state

    def set_apex_level_line_state(self, state):
        self._apex_level_line_state = state

    def set_ruler_state(self, state):
        self._ruler_state = state

    def set_cm_number(self, number):
        self._cm_number = number

# GETTERS:

    def get_h(self):
        return self._h

    def get_scaled_h(self):
        return self._scaled_h

    def get_scale_coeff(self):
        return self._scale_coeff

    def get_object(self):
        return self._images_list[self._current_slice_number]

    def calculate_scale_coeff(self):
        if self._ruler_state:
            self._scale_coeff_list[self._current_slice_number] = \
                self._cm_number/self._ruler.GetDistanceRepresentation().GetDistance()
            self._scale_coeff = self.list_average(self._scale_coeff_list)

# SCENE UPDATING:

    def _set_references(self):
        # set references according to current image (slice) number
        self._current_slice = self._images_list[self._current_slice_number]
        self._current_renderer = self._renderer_list[self._current_slice_number]

    def update(self):
        """
        Update vtk scene (called if the object was changed/switched)
        """
        self._set_references()
        self._set_movable_lines_renderers()
        self._set_backlight_handles_renderers()

    def _set_movable_lines_renderers(self):
        self._spin_axis_list[self._current_slice_number].connect_with_renderer(self._current_renderer)
        self._base_lines_list[self._current_slice_number].connect_with_renderer(self._current_renderer)

# BACKLIGHT HANDLES:

    def _initialize_backlight_handles(self):
        handle_size = 5.
        apex_point_color = [0, 1, 0]
        self._apex_point_widget = BacklightHandleWidget(apex_point_color, handle_size)
        self._apex_point_widget.SetInteractor(self._interactor)
        base_point_color = [0, 1, 1]
        self._base_point_widget_1 = BacklightHandleWidget(base_point_color, handle_size)
        self._base_point_widget_1.SetInteractor(self._interactor)
        self._base_point_widget_2 = BacklightHandleWidget(base_point_color, handle_size)
        self._base_point_widget_2.SetInteractor(self._interactor)

    def _set_backlight_handles_renderers(self):
        self._apex_point_widget.connect_with_renderer(self._current_renderer)
        self._base_point_widget_1.connect_with_renderer(self._current_renderer)
        self._base_point_widget_2.connect_with_renderer(self._current_renderer)

# RULER:

    def _initialize_ruler(self):
        self._ruler = vtk.vtkDistanceWidget()
        self._ruler.CreateDefaultRepresentation()
        self._ruler.SetInteractor(self._interactor)

    def _vtk_observer_call_ruler(self, obj, event):
        if self._ruler_state:
            self._ruler.On()
        else:
            self._ruler.Off()
        self._interactor.Initialize()

# LABEL LINES:

    def _initialize_label_lines(self, renderer):
        self._spin_axis_list.append(MovableLine([1, 0, 0]))
        self._spin_axis_list[-1].connect_with_renderer(renderer)
        self._base_lines_list.append(MovableLine([1, 0, 0]))
        self._base_lines_list[-1].connect_with_renderer(renderer)
        self._apex_level_line.append(MovableLine([0.7, 0.9, 0.4]))
        self._apex_level_line[-1].connect_with_renderer(renderer)

    def _compute_label_lines(self):
        if self._apex_point_widget.GetEnabled() and \
                self._base_point_widget_1.GetEnabled() and \
                self._base_point_widget_2.GetEnabled():
            point_1 = self._base_point_widget_1.get_position()
            point_2 = self._base_point_widget_2.get_position()
            point_3 = self._apex_point_widget.get_position()
            spin_axis_normal = self._normalize_vector(self._normal_to_line(point_1, point_2))

            spin_ax_p1 = point_3
            spin_ax_p2 = [point_3[i] + spin_axis_normal[i] for i in range(3)]
            intersection = [[0, 0, 0], [0, 0, 0]]
            t1 = vtk.mutable(0)
            t2 = vtk.mutable(0)
            vtk.vtkLine.DistanceBetweenLines(point_1, point_2, spin_ax_p1, spin_ax_p2,
                                             intersection[0], intersection[1], t1, t2)

            self._spin_axis_list[self._current_slice_number].set_point_2(point_3)
            self._spin_axis_list[self._current_slice_number].set_point_1(intersection[0])
            self._base_lines_list[self._current_slice_number].set_point_1(point_1)
            self._base_lines_list[self._current_slice_number].set_point_2(point_2)

# MARKING (to construct spin axis and base axis):

    def marking(self, point):
        """
        Mark apex and two base points to define spin axis and base axis
        """
        if self._apex_point_widget.GetEnabled():
            if self._base_point_widget_1.GetEnabled():
                if not self._base_point_widget_2.GetEnabled():
                    self._base_point_widget_2.On()
                    self._base_point_widget_2.set_position(point)
                    self._compute_label_lines()
            else:
                self._base_point_widget_1.On()
                self._base_point_widget_1.set_position(point)
        else:
            self._apex_point_widget.On()
            self._apex_point_widget.set_position(point)

    def vtk_observer_marking(self, obj, event):
        if not self._marking_state:
            return
        self.marking(self._interactor_style.get_picked_position())

    def remove_marks(self):
        """
        Remove all marks form the scene
        """
        self._apex_point_widget.Off()
        self._base_point_widget_1.Off()
        self._base_point_widget_2.Off()
        self._interactor.Initialize()

# APEX THICKNESS:

    def add_level_line(self):
        """
        Add line to mark apex thickness
        """
        if self._apex_level_line_state:
            picked_position = list(self._interactor_style.get_picked_position())
            picked_position[0] = 0
            picked_position[2] = 0
            pos_y = picked_position[1]
            span = 8
            self._apex_level_line[self._current_slice_number].set_point_1([-span, pos_y, 0])
            self._apex_level_line[self._current_slice_number].set_point_2([span, pos_y, 0])
            self.set_h(pos_y)
            self._interactor.Initialize()
        else:
            self._remove_level_line()

    def _remove_level_line(self):
        if "_current_renderer" in self.__dict__:
            # self._current_renderer.RemoveActor(self._level_line_actor)
            self._interactor.Initialize()

    def vtk_observer_add_level_line(self, obj, event):
        self.add_level_line()

# CHANGE OF COORDINATE SYSTEM:

    def rotate_image_to_axis(self):
        """
        Rotate an image to change coordinate system (affine transformation)
        """
        if not (self._apex_point_widget.GetEnabled() and
                    self._base_point_widget_1.GetEnabled() and
                    self._base_point_widget_2.GetEnabled()):
            return
        target_vector = [0, 1, 0]   # axis y
        control_vector = [0, 0, 1]  # axis z, for the triple product
        image = self._current_slice
        self._compute_label_lines()
        spin_axis = self._spin_axis_list[self._current_slice_number]  # [0] - object, [1] - actor
        base_line = self._base_lines_list[self._current_slice_number]

        spin_axis_vector = [(spin_axis.get_point_1()[i] - spin_axis.get_point_2()[i]) for i in range(3)]
        spin_axis_vector = self._normalize_vector(spin_axis_vector)
        angle = self._angle_between_vectors(target_vector, spin_axis_vector)

        tr_pr = self._triple_product(target_vector, spin_axis_vector, control_vector)
        if tr_pr < 0:
            angle *= -1

        camera = self._current_renderer.GetActiveCamera()
        camera.Roll(degrees(angle))
        self._camera_rotation_list[self._current_slice_number] += angle

        aligned_image = self._translate_and_rotate_image(image, spin_axis.get_point_2(), angle)

        self._current_slice = aligned_image
        self._images_list[self._current_slice_number] = aligned_image

        camera.Zoom(3.0)  # image extent is changing and camera becomes very far
        # 3.0 value is arbitrarily

        self._redraw_label_lines(spin_axis, base_line)

    def _translate_and_rotate_image(self, image, apex_point, angle):
        transform = vtk.vtkTransform()
        transform.Translate(apex_point)
        transform.RotateZ(degrees(angle))

        reslice = vtk.vtkImageReslice()
        reslice.SetInterpolationModeToCubic()
        reslice.SetInputData(image)
        reslice.SetResliceTransform(transform)
        # When image is transform, it's extent doesn't changing
        # Current implementation of extents changing can be a bit rough
        reslice.SetOutputExtent(-self._image_extent_list[self._current_slice_number][1],
                                self._image_extent_list[self._current_slice_number][1],
                                -self._image_extent_list[self._current_slice_number][3],
                                self._image_extent_list[self._current_slice_number][3],
                                0, 0)
        reslice.SetOutputOrigin(0, 0, 0)
        reslice.Update()

        return reslice.GetOutput()

    def _redraw_label_lines(self, spin_axis, base_line):
        spin_axis_width = self._distance(spin_axis.get_point_1(), spin_axis.get_point_2())

        spin_axis.set_point_1([0, spin_axis_width, 0])
        spin_axis.set_point_2([0, 0, 0])
        base_line.set_point_1([-0.4 * spin_axis_width, spin_axis_width, 0])
        base_line.set_point_2([0.4 * spin_axis_width, spin_axis_width, 0])
        self._base_point_widget_1.set_position(base_line.get_point_1())
        self._base_point_widget_2.set_position(base_line.get_point_2())
        self._apex_point_widget.set_position([0, 0, 0])

        self._interactor.Initialize()

# STATIC METHODS:

    @staticmethod
    def _normalize_vector(vector):
        norm = sqrt(vector[0] ** 2 + vector[1] ** 2 + vector[2] ** 2)
        if norm == 0:
            print ("Division by zero")
            return vector
        unit_vector = [vector[0] / norm, vector[1] / norm, vector[2] / norm]
        return unit_vector

    @staticmethod
    def _angle_between_vectors(vector1, vector2):
        angle = vtk.vtkMath.AngleBetweenVectors(vector1, vector2)
        return angle

    @staticmethod
    def _reverse_vector(vector):
        r_vector = [-i for i in vector]
        return r_vector

    @staticmethod
    def _distance(point_1, point_2):
        return sqrt(vtk.vtkMath.Distance2BetweenPoints(point_1,
                                                       point_2))

    @staticmethod
    def _triple_product(vector_1, vector_2, vector_3):
        matrix_ = matrix([vector_1, vector_2, vector_3])
        determine = det(matrix_)
        return determine

    @staticmethod
    def _normal_to_line(point_1, point_2):
        # constructing line equation by two points,
        # normal is n(A, B) (A and B from line equation)
        return [point_1[1] - point_2[1],
                point_2[0] - point_1[0],
                0]  # for 3D space

    @staticmethod
    def _find_closest_point(target_point, points_list):
        distance2 = vtk.vtkMath.Distance2BetweenPoints
        closest_point = points_list[0]
        if len(points_list) > 1:
            for point in points_list[1:]:
                if distance2(target_point, closest_point) > distance2(target_point, point):
                    closest_point = point
        return closest_point

    @staticmethod
    def list_average(ls):
        # important note:
        # Because we have zeros list initially, but h and z can not be 0,
        # then we ignore all zeros to find average correctly
        ls = filter(lambda i: i > 0, ls)
        if len(ls) == 0:
            return 0
        return sum(ls) / len(ls)

    @staticmethod
    def _get_image_extent(image):
        return list(image.GetExtent())
