from vtk import vtkLineSource, vtkSphereWidget


class LevelLineWidget(vtkSphereWidget):
    def __init__(self):
        self.SetRepresentationToSurface()
        self.SetRadius(1)

        self.line = vtkLineSource()
        self._movable_axis = 0
        self._span_value = 1.
        self._initial_pos = [0, 0, 0]

        self.set_center(self._initial_pos)
        self._widget_pos = self._initial_pos

        self.AddObserver("InteractionEvent", self._vtk_observer_widget_get_offset)

    def set_center(self, point_coordinates):
        self.SetCenter(point_coordinates)
        self._widget_pos = point_coordinates
        self._move_line_for_the_handle()

    def get_center(self):
        return self._widget_pos

    def set_line_span(self, span_value):
        self._span_value = span_value
        self._move_line_for_the_handle()

    def _move_line_for_the_handle(self):
        # Works for XOY
        pos = self._widget_pos
        span_value = self._span_value
        if self._movable_axis == 1:
            self.line.SetPoint1(-span_value, pos[1], 0)
            self.line.SetPoint2(span_value, pos[1], 0)
            return
        if self._movable_axis == 0:  # without "if not self._movable_axis:" to make it more clear
            self.line.SetPoint1(pos[0], -span_value, 0)
            self.line.SetPoint2(pos[0], span_value, 0)
            return

    def set_movable_axis(self, axis):
        # axis: 0 - x, 1 - y, z - 2
        self._movable_axis = axis

    def _widget_get_offset(self):
        current_pos = self.GetCenter()
        correct_pos = [self._initial_pos[i] if i != self._movable_axis else current_pos[i]
                       for i in range(3)]
        self.SetCenter(correct_pos)
        self._widget_pos = correct_pos
        self._move_line_for_the_handle()

    def _vtk_observer_widget_get_offset(self, obj, event):
        self._widget_get_offset()

    def _set_renderer(self, renderer):
        self._renderer = renderer
