import vtk


class MovableLine:
    def __init__(self, color):
        self._source = vtk.vtkLineSource()
        self._mapper = vtk.vtkPolyDataMapper()
        self._actor = vtk.vtkActor()
        self._renderer = None

        self._actor.GetProperty().SetColor(color)
        self._mapper.SetInputConnection(self._source.GetOutputPort())
        self._actor.SetMapper(self._mapper)

    def connect_with_renderer(self, renderer):
        self._renderer = renderer
        self._renderer.RemoveActor(self._actor)
        self._renderer.AddActor(self._actor)

    def disconnect_with_renderer(self):
        self._renderer.RemoveActor(self._actor)
        self._renderer = None

    def set_point_1(self, coord_list):
        self._source.SetPoint1(coord_list)

    def set_point_2(self, coord_list):
        self._source.SetPoint2(coord_list)

    def get_point_1(self):
        return self._source.GetPoint1()

    def get_point_2(self):
        return self._source.GetPoint2()

    def get_actor(self):
        return self._actor
