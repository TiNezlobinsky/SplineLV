import vtk


class BacklightHandleWidget(vtk.vtkHandleWidget):

    def __init__(self, color, handle_size):
        self.CreateDefaultRepresentation()
        self.GetHandleRepresentation().GetProperty().SetColor(color)
        self.GetHandleRepresentation().SetHandleSize(handle_size)
        self._initialize_point_widget_backlight(color, handle_size)

        self.AddObserver("InteractionEvent", self._widget_get_offset)

    def connect_with_renderer(self, renderer):
        self._renderer = renderer

    def set_position(self, position):
        self.GetHandleRepresentation().SetWorldPosition(position)
        self._widget_backlight_source.SetCenter(position)

    def get_position(self):
        return self.GetHandleRepresentation().GetWorldPosition()

    def _initialize_point_widget_backlight(self, color, handle_size):
        self._widget_backlight_source = vtk.vtkSphereSource()
        self._widget_backlight_source.SetRadius(handle_size)
        self._widget_backlight_mapper = vtk.vtkDataSetMapper()
        self._widget_backlight_actor = vtk.vtkActor()

        self._widget_backlight_mapper.SetInputConnection(self._widget_backlight_source.GetOutputPort())
        self._widget_backlight_actor.SetMapper(self._widget_backlight_mapper)
        self._widget_backlight_actor.GetProperty().SetColor(color)
        self._widget_backlight_actor.GetProperty().SetOpacity(0.5)

    def _widget_get_offset(self, obj, event):
        position = self.GetHandleRepresentation().GetWorldPosition()
        self._widget_backlight_source.SetCenter(position)
        self.GetInteractor().Initialize()

    def On(self):
        vtk.vtkHandleWidget.On(self)
        self._renderer.AddActor(self._widget_backlight_actor)
        self.GetInteractor().Initialize()

    def Off(self):
        vtk.vtkHandleWidget.Off(self)
        self._renderer.RemoveActor(self._widget_backlight_actor)
        self.GetInteractor().Initialize()

