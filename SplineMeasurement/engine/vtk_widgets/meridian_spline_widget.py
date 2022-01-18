import vtk
from SplineMeasurement.engine.vtk_widgets.ro_psi_spline_widget import RoPsiSplineWidget


# CODE REGIONS:
# 1) Initialization
# 2) Setters
# 3) Getters:
# 4) Spline management
# 5) Meridian modes
# 6) Vtk observers


class MeridianSplineWidget:
    """
    Unites epi and endo spline to maintain an equal height.
    Spline management occurs through this class
    """
    def __init__(self, side, epi_spline_color, endo_spline_color):
        self._side = side
        self._epi_spline_color = epi_spline_color
        self._endo_spline_color = endo_spline_color

        self._initialze_states()

        self._vtk_scene = None

# INITIALIZATION:

    def _initialize_vtk_events(self):
        self._vtk_scene.AddObserver("LeftButtonPressEvent", self.vtk_observer_set_endo_handle_position)
        self._vtk_scene.AddObserver("LeftButtonPressEvent", self.vtk_observer_set_epi_handle_position)
        self._vtk_scene.AddObserver("RightButtonPressEvent", self.vtk_observer_delete_endo_handle)
        self._vtk_scene.AddObserver("RightButtonPressEvent", self.vtk_observer_delete_epi_handle)

    def _initialze_states(self):
        self._epi_editable = False
        self._endo_editable = False

    def initialize_splines(self):
        spl_seg_dist = 25
        if self._side == "right":
            side_coeff = 1
        else:
            side_coeff = -1
        self._init_endo_handles_positions = [[0, self._h, 0],
                                             [side_coeff * 20, 20, 0],
                                             [side_coeff * 35, 50, 0],
                                             [side_coeff * 45, 90, 0]]
        self._init_epi_handles_positions = [[0, 0, 0],
                                            [side_coeff * 40, 20, 0],
                                            [side_coeff * 70, 50, 0],
                                            [side_coeff * 90, 90, 0]]

        endo_pattern = self._create_spline_pattern(line_color=self._endo_spline_color, line_width=3,
                                                   handle_color=self._endo_spline_color, handle_opacity=0.4,
                                                   handle_positions=self._init_endo_handles_positions)
        epi_pattern = self._create_spline_pattern(line_color=self._epi_spline_color, line_width=3,
                                                  handle_color=self._epi_spline_color, handle_opacity=0.4,
                                                  handle_positions=self._init_epi_handles_positions)

        self._endo_spline = self._create_spline_widget('endo', endo_pattern, 1.0)
        self._endo_spline.SetInteractor(self._interactor)
        self._endo_spline.set_render(self._renderer)
        self._epi_spline = self._create_spline_widget('epi', epi_pattern, 0.0)
        self._epi_spline.SetInteractor(self._interactor)
        self._epi_spline.set_render(self._renderer)

        self._endo_spline.connect_with_spline(self._epi_spline)
        self._epi_spline.connect_with_spline(self._endo_spline)

        self._initialize_vtk_events()

    def _create_spline_pattern(self, line_color, line_width, handle_color, handle_opacity, handle_positions):
        pattern = dict()
        pattern['line_color'] = line_color
        pattern['line_width'] = line_width
        pattern['handle_color'] = handle_color
        pattern['handle_opacity'] = handle_opacity
        pattern['first_handle_position'] = handle_positions[0]
        pattern['second_handle_position'] = handle_positions[1]
        pattern['third_handle_position'] = handle_positions[2]
        pattern['fourth_handle_position'] = handle_positions[3]
        return pattern

    def _create_spline_widget(self, spline_type, pattern, gamma):
        spline = RoPsiSplineWidget(self._side, spline_type)

        line_property = spline.GetLineProperty()
        line_property.SetColor(pattern['line_color'])
        line_property.SetLineWidth(pattern['line_width'])
        handle = spline.GetHandleProperty()
        handle.SetColor(pattern['handle_color'])
        handle.SetOpacity(pattern['handle_opacity'])
        first_handle_position = pattern['first_handle_position']
        second_handle_position = pattern['second_handle_position']
        third_handle_position = pattern['third_handle_position']
        fourth_handle_position = pattern['fourth_handle_position']

        # We first need to set Z and h and then add handles!
        spline.set_Z(self._Z)
        spline.set_h(self._h)
        spline.set_gamma(gamma)
        spline.set_render(self._renderer)

        spline.add_handle(first_handle_position)
        spline.add_handle(second_handle_position)
        spline.add_handle(third_handle_position)
        spline.add_handle(fourth_handle_position)

        return spline

# SETTERS:

    def set_interactor(self, interactor):
        self._interactor = interactor
        self._interactor_style = self._interactor.GetInteractorStyle()

    def set_renderer(self, renderer):
        self._renderer = renderer

    def set_vtk_scene(self, vtk_scene):
        self._vtk_scene = vtk_scene

    def set_Z(self, z):
        self._Z = z

    def set_h(self, h):
        self._h = h

# GETTERS:

    def get_Z(self):
        return self._endo_spline.get_Z()

    def get_h(self):
        return self._h

    def get_epi_z_coordinates(self):
        return self._epi_spline.get_z_coordinates()

    def get_endo_z_coordinates(self):
        return self._endo_spline.get_z_coordinates()

    def get_epi_ro_coordinates(self):
        return self._epi_spline.get_ro_coordinates()

    def get_endo_ro_coordinates(self):
        return self._endo_spline.get_ro_coordinates()

    def get_epi_psi_coordinates(self):
        return self._epi_spline.get_psi_coordinates()

    def get_endo_psi_coordinates(self):
        return self._endo_spline.get_psi_coordinates()

    def get_epi_spline_ref(self):
        return self._epi_spline.get_spline_object()

    def get_endo_spline_ref(self):
        return self._endo_spline.get_spline_object()

# SPLINE MANAGEMENT:

    def update_h(self, h):
        self._h = h
        self._epi_spline.set_h(self._h)
        self._endo_spline.set_h(self._h)

    def activate(self):
        self._endo_spline.On()
        self._epi_spline.On()

    def inactivate(self):
        self._endo_spline.Off()
        self._epi_spline.Off()

# HANDLES MANAGEMENT:

    def reset(self):
        self._epi_spline.SetNumberOfHandles(4)
        self._epi_spline.set_spline_nodes(self._init_epi_handles_positions)

        self._endo_spline.SetNumberOfHandles(4)
        self._endo_spline.set_spline_nodes(self._init_endo_handles_positions)

    def set_epi_spline_handle_position(self):
        position = self._interactor_style.get_picked_position()
        if self._epi_spline.GetEnabled():
            self._epi_spline.add_handle(position)

    def set_endo_spline_handle_position(self):
        position = self._interactor_style.get_picked_position()
        if self._endo_spline.GetEnabled():
            self._endo_spline.add_handle(position)

    def delete_epi_spline_handle(self):
        position = self._interactor_style.get_picked_position()
        handles_position_list = self._epi_spline.get_handles_position_list()
        if self._epi_spline.GetEnabled():
            closest_point = self._find_closest_point(position, handles_position_list)
            self._epi_spline.delete_handle(closest_point)

    def delete_endo_spline_handle(self):
        position = self._interactor_style.get_picked_position()
        handles_position_list = self._endo_spline.get_handles_position_list()
        if self._endo_spline.GetEnabled():
            closest_point = self._find_closest_point(position, handles_position_list)
            self._endo_spline.delete_handle(closest_point)

# MERIDIAN MODES:

    def epi_is_editable(self):
        return self._epi_editable

    def endo_is_editable(self):
        return self._endo_editable

    def epi_spline_interaction_on(self):
        self._epi_spline.ProcessEventsOn()
        self._epi_editable = False

    def endo_spline_interaction_on(self):
        self._endo_spline.ProcessEventsOn()
        self._endo_editable = False

    def epi_spline_interaction_off(self):
        self._epi_spline.ProcessEventsOff()
        self._epi_editable = True

    def endo_spline_interaction_off(self):
        self._endo_spline.ProcessEventsOff()
        self._endo_editable = True

# VTK OBSERVERS:
# Note: obj and event args are used by vtk observer, don't delete it

    def vtk_observer_set_epi_handle_position(self, obj, event):
        if self.epi_is_editable():
            self.set_epi_spline_handle_position()

    def vtk_observer_set_endo_handle_position(self, obj, event):
        if self.endo_is_editable():
            self.set_endo_spline_handle_position()

    def vtk_observer_delete_endo_handle(self, obj, event):
        if self.endo_is_editable():
            self.delete_endo_spline_handle()

    def vtk_observer_delete_epi_handle(self, obj, event):
        if self.epi_is_editable():
            self.delete_epi_spline_handle()

    @staticmethod
    def _find_closest_point(target_point, points_list):
        distance2 = vtk.vtkMath.Distance2BetweenPoints
        closest_point = points_list[0]
        if len(points_list) > 1:
            for point in points_list[1:]:
                if distance2(target_point, closest_point) > distance2(target_point, point):
                    closest_point = point
        return closest_point
