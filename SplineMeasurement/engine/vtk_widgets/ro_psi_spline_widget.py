from vtk import vtkSplineWidget, vtkLineSource, vtkActor, vtkPolyDataMapper
from numpy import linspace
from math import pi, asin, sqrt, sin
from scipy import interpolate
import numpy as np


# CODE REGIONS:
# 1) Spline computing
# 2) Spline redrawing
# 3) Setters
# 4) Getters
# 5) Coordinates transformation
# 6) Handles management
# 7) Neighboring spline connection


class RoPsiSplineWidget(vtkSplineWidget):
    """
    Interactive spline for contouring left ventricle wall.

    Handles (spline nodes) used to manage spline interactively
    """
    def __init__(self, side, spline_type):
        # side = 'right' or 'left'
        # spline_type = 'endo' or 'epi' only
        if side == "left":
            self._sign = -1
        else:
            self._sign = 1
        self._spline_type = spline_type
        self.psi_interval_points = 60
        self.ro_nodes_array = np.array([])
        self.psi_nodes_array = np.array([])
        self.z_nodes_array = np.array([])
        self.ro_array = np.array([])
        self.psi_array = np.array([])
        self.output_spline_points = []
        self.line_source_list = []
        self.actor_list = []
        self.mapper_list = []
        self._handles_position_list = []
        self._neighboring_spline = None

        self.AddObserver("InteractionEvent", self._vtk_observer_remember_handles_position)
        self.AddObserver("InteractionEvent", self._vtk_observer_compute)
        self.AddObserver("InteractionEvent", self._vtk_observer_move_neighboring_spline_handle)

    def Off(self):
        vtkSplineWidget.Off(self)
        for actor in self.actor_list:
            self.render.RemoveActor(actor)
        self.GetInteractor().Initialize()

# SPLINE COMPUTING:

    def _compute_ro_psi_spline(self):
        self.psi_nodes_array = self.psi_nodes_array[::-1]  # reverse array
        self.ro_nodes_array = self.ro_nodes_array[::-1]
        self.z_nodes_array = self.z_nodes_array[::-1]

        psi_0 = 0.
        psi_1 = pi/2.

        psi_array = linspace(psi_0, psi_1, self.psi_interval_points)
        psi_array = sorted(psi_array)

        self._tck = interpolate.splrep(self.psi_nodes_array, self.ro_nodes_array, s=0)  # for b-spline
        output_ro = interpolate.splev(psi_array, self._tck)

        self._interpolate = interpolate.splev

        self.ro_array = output_ro
        self.psi_array = psi_array

    def compute(self):
        """
        Compute spline for current handles
        """
        try:
            if self.GetNumberOfHandles() > 3:  # we need at least 4 point to build cubic spline
                spline_handles = self.GetNumberOfHandles()
                pos = self.GetHandlePosition(spline_handles - 1)
                self.Z = pos[1]
                self._fix_first_handle()
                self._handles_coordinates_to_ropsi()
                self._compute_ro_psi_spline()
                self._ropsi_to_xyz()
                self._update_spline()
        except Exception:
            pass

    def _vtk_observer_compute(self, obj, event):
        self.compute()

# SPLINE REDRAWING:

    def _update_spline(self):
        for actor in self.actor_list:
            self.render.RemoveActor(actor)
        self.line_source_list = []
        self.actor_list = []
        self.mapper_list = []
        self._draw_spline()

    def _draw_spline(self):
        for i in range(len(self.output_spline_points[0]) - 1):
            self.line_source_list.append(vtkLineSource())
            self.actor_list.append(vtkActor())
            self.mapper_list.append(vtkPolyDataMapper())

        spline_color = self.GetLineProperty().GetColor()
        spline_width = self.GetLineProperty().GetLineWidth()
        for i, line in enumerate(self.line_source_list):
            x1 = self.output_spline_points[0][i]
            y1 = self.output_spline_points[1][i]
            z1 = self.output_spline_points[2][i]
            x2 = self.output_spline_points[0][i + 1]
            y2 = self.output_spline_points[1][i + 1]
            z2 = self.output_spline_points[2][i + 1]
            line.SetPoint1(x1, y1, 0)
            line.SetPoint2(x2, y2, 0)
            self.mapper_list[i].SetInputConnection(line.GetOutputPort())
            self.actor_list[i].SetMapper(self.mapper_list[i])
            self.actor_list[i].GetProperty().SetColor(spline_color)
            self.actor_list[i].GetProperty().SetLineWidth(spline_width)
            self.render.AddActor(self.actor_list[i])
        self.GetLineProperty().SetOpacity(0.01)
        self.GetInteractor().Initialize()

# SETTERS:

    def set_psi_interval_points(self, n):
        self.psi_interval_points = n

    def set_spline_nodes(self, node_list, compute_=True):
        for i in range(len(node_list)):
            self.SetHandlePosition(i, *node_list[i])
        if compute_:
            self.compute()

    def set_h(self, h):
        self.h = h

    def set_Z(self, z):
        spline_handles = self.GetNumberOfHandles()
        pos = list(self.GetHandlePosition(spline_handles - 1))
        pos[1] = z
        self.SetHandlePosition(spline_handles - 1, pos)
        self.Z = z
        self._remember_handles_position()
        if self.GetEnabled():
            self.compute()

    def set_gamma(self, gamma):
        self.gamma = gamma

    def set_render(self, render):
        self.render = render

# GETTERS:

    def get_h(self):
        return self.h

    def get_Z(self):
        return self.Z

    def get_ropsi_handles_coordinates(self):
        return [self.ro_nodes_array, self.psi_nodes_array, self.z_nodes_array]

    def get_ropsi_set(self):
        return [self.ro_array, self.psi_array]

    def get_z_set(self):
        z_set = self.Z - (self.Z - self.h * self.gamma) * np.sin(self.psi_array)
        return z_set

    def get_ro_set(self):
        return self.ro_array

    def get_psi_set(self):
        return self.psi_array

    def get_psi_coordinates(self):
        return self.psi_nodes_array

    def get_ro_coordinates(self):
        return self.ro_nodes_array

    def get_z_coordinates(self):
        return self.z_nodes_array

    def get_handles_position_list(self):
        return self._handles_position_list

    def get_handles_number(self):
        # May be should use the original GetNumberOfHandles()?
        return len(self._handles_position_list)

    def get_spline_set(self):
        return [list(self.ro_array), list(self.psi_array)]

    def get_spline_object(self):
        return [self._tck, self._interpolate]

# COORDINATES TRANSFORMATION:

    def _handles_coordinates_to_ropsi(self):
        self.psi_nodes_array = np.array([])
        self.ro_nodes_array = np.array([])
        self.z_nodes_array = np.array([])
        number_of_points = self.GetNumberOfHandles()
        for i in range(number_of_points):
            x = self.GetHandlePosition(i)[0]  # why not in the single line?
            y = self.GetHandlePosition(i)[1]
            z = self.GetHandlePosition(i)[2]
            arg = (self.Z - y) / (self.Z - self.h * self.gamma)
            if arg > 1.0:
                arg = 1.0
            psi = asin(arg)
            ro = sqrt(x ** 2)
            self.psi_nodes_array = np.append(self.psi_nodes_array, psi)
            self.ro_nodes_array = np.append(self.ro_nodes_array, ro)
            self.z_nodes_array = np.append(self.z_nodes_array, y)

    def _ropsi_to_xyz(self):
        x = []
        y = []
        z = []
        for i in range(len(self.psi_array)):
            y.append(self.Z - (self.Z - self.h * self.gamma) * sin(self.psi_array[i]))
            x.append(self._sign * sqrt(self.ro_array[i] ** 2))
            z.append(self.GetHandlePosition(0)[2])
        self.output_spline_points = [x, y, z]

# HANDLES MANAGEMENT:

    def _fix_first_handle(self):
        # Subsequent algorithm requires fixing
        # of the first point of the spline
        if self._spline_type == 'endo':
            self.SetHandlePosition(0, 0., self.h, 0.)
        else:
            self.SetHandlePosition(0, 0., 0., 0.)

    def _remember_handles_position(self):
        # We have to dynamically track the position of spline handles and write at list
        handles_number = len(self._handles_position_list)
        self._handles_position_list = []
        for i in range(handles_number):
            self._handles_position_list.append(self.GetHandlePosition(i))

    def _vtk_observer_remember_handles_position(self, obj, event):
        self._remember_handles_position()

    def add_handle(self, position):
        """
        Add new handle in specified position

        Parameters
        ----------
        position : array_like
            (x, y, z) to append to handles list
        """
        position = list(position)
        position[2] = 0
        self._handles_position_list.append(position)
        self._update_spline_handles_position()

    def delete_handle(self, position):
        """
        Delete new handle from specified position

        Parameters
        ----------
        position : array_like
            (x, y, z) to delete from handles list
        """
        position = list(position)
        position[2] = 0
        self._handles_position_list.remove(position)
        self._update_spline_handles_position()

    def _update_spline_handles_position(self):
        self._handles_position_list.sort(key=lambda k: k[1])  # we use sorting by y component
        handles_number = len(self._handles_position_list)
        if handles_number > 1:  # otherwise it raise warning when points count become less than 2
            self.SetNumberOfHandles(handles_number)
            for i in range(handles_number):
                self.SetHandlePosition(i, self._handles_position_list[i])
            if self.GetEnabled():
                self.compute()

    def remove_all_handles(self):
        """
        Remove all handles from handles list
        """
        self._handles_position_list = []

# NEIGHBORING SPLINE CONNECTION:

    def connect_with_spline(self, spline):
        """
        Connect with neighboring endo/epi spline to to maintain an equal height (Z)
        on the same meridian

        Parameters
        ----------
        spline : RoPsiSplineWidget object
        """
        self._neighboring_spline = spline
        self.set_Z(spline.get_Z())

    def _move_neighboring_spline_handle(self):
        self._neighboring_spline.set_Z(self.get_Z())

    def _vtk_observer_move_neighboring_spline_handle(self, obj, event):
        self._move_neighboring_spline_handle()
