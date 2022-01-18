import vtk
from math import sin, cos, asin


class PsiLevelWidget(vtk.vtkSphereWidget):
    def __init__(self, gamma):
        self._endo_ro_set = []
        self._endo_psi_set = []
        self._epi_ro_set = []
        self._epi_psi_set = []
        self._z = 1.
        self._h = 1.
        self._gamma = gamma
        self._psi_pos = 0
        self._sign = 1
        initial_pos = [0, 0, 0]
        self.GetCenter(initial_pos)
        self._initial_pos = initial_pos
        self._widget_pos = initial_pos
        self._movable_axis = 1
        self._fixed_axis = 0
        self._handle_offset = 0

        self.SetRadius(5)
        self.SetRepresentationToSurface()

        self._line_source = vtk.vtkLineSource()
        self._line_actor = vtk.vtkActor()
        self._line_mapper = vtk.vtkDataSetMapper()

        self._renderer = None

        self.AddObserver("InteractionEvent", self._vtk_observer_widget_get_offset)

    def get_z(self):
        return self._z

    def get_h(self):
        return self._h

    def get_psi(self):
        return self._psi_pos

    def set_endo_spline_set(self, spline_set):
        self._endo_ro_set = spline_set[0]
        self._endo_psi_set = spline_set[1]

    def set_epi_spline_set(self, spline_set):
        self._epi_ro_set = spline_set[0]
        self._epi_psi_set = spline_set[1]

    def set_epi_spline_object(self, spline_object):
        self._epi_tck = spline_object[0]
        self._epi_interpolate = spline_object[1]

    def set_endo_spline_object(self, spline_object):
        self._endo_tck = spline_object[0]
        self._endo_interpolate = spline_object[1]

    def set_z(self, z):
        self._z = z

    def set_h(self, h):
        self._h = h

    def set_movable_axis(self, axis):
        self._movable_axis = axis

    def set_fixed_axis(self, axis):
        self._fixed_axis = axis

    def set_handle_offset(self, offset):
        self._handle_offset = offset

    def set_color(self, color):
        self.GetSphereProperty().SetOpacity(0.5)
        self.GetSphereProperty().SetColor(color)
        self._line_actor.GetProperty().SetColor(color)

    def reflected(self):
        self._sign = -1

    def origin(self):
        self._sign = 1

    def _widget_get_offset(self):
        current_pos = self.GetCenter()
        correct_pos = [self._initial_pos[i] if i != self._movable_axis else current_pos[i]
                       for i in range(3)]
        if correct_pos[self._movable_axis] > self._z:
            correct_pos[self._movable_axis] = self._z
        elif correct_pos[self._movable_axis] < self._h*self._gamma:
            correct_pos[self._movable_axis] = self._h*self._gamma
        correct_pos[self._fixed_axis] = self._handle_offset
        self.SetCenter(correct_pos)
        self._compute_line_points(correct_pos)
        self.GetInteractor().Initialize()

    def _vtk_observer_widget_get_offset(self, obj, event):
        self._widget_get_offset()

    def _compute_line_points(self, correct_pos):
        try:
            endo_psi = self._compute_psi(correct_pos[1], 1)
            epi_psi = self._compute_psi(correct_pos[1], 0)

            endo_ro = self._endo_interpolate([endo_psi], self._endo_tck)
            epi_ro = self._epi_interpolate([endo_psi], self._epi_tck)

            point_1_x = self._sign*endo_ro[0]
            point_1_y = self._z - (self._z - self._h)*sin(endo_psi)
            point_1_z = 0
            point_2_x = self._sign*epi_ro[0]
            point_2_y = self._z - self._z*sin(endo_psi)
            point_2_z = 0

            self._line_point_1 = [point_1_x, point_1_y, point_1_z]
            self._line_point_2 = [point_2_x, point_2_y, point_2_z]
            self._line_source.SetPoint1(self._line_point_1)
            self._line_source.SetPoint2(self._line_point_2)
            self._psi_pos = endo_psi
        except Exception:
            pass

    def _initialize_line(self):
        self._line_mapper.SetInputConnection(self._line_source.GetOutputPort())
        self._line_actor.SetMapper(self._line_mapper)
        self._line_actor.GetProperty().SetLineWidth(3.)
        # maybe try - exception block?
        self._renderer.AddActor(self._line_actor)
        self.GetInteractor().Initialize()

    def On(self):
        vtk.vtkSphereWidget.On(self)
        self._initialize_line()
        # self._compute_line_points()

    def Off(self):
        vtk.vtkSphereWidget.Off(self)
        self._renderer.RemoveActor(self._line_actor)
        self.GetInteractor().Initialize()
        self._widget_get_offset()

    def set_position(self, position):
        self._initial_pos = position
        self._widget_pos = position
        self.SetCenter(position)

    def SetInteractor(self, interactor):
        vtk.vtkSphereWidget.SetInteractor(self, interactor)

    def set_renderer(self, renderer):
        self._renderer = renderer

    def _compute_psi(self, z, gamma):
        arg = (self._z - z)/(self._z - self._h*gamma)
        if arg > 1.0:
            arg = 1.0
        return asin(arg)

    def _find_closest_psi(self, target_psi, psi_set):
        diff_list = [abs(psi - target_psi) for psi in psi_set]
        min_value = min(diff_list)
        index = diff_list.index(min_value)
        closest = psi_set[index]
        return closest, index
