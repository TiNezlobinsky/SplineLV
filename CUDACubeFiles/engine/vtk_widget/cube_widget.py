import vtk


class CubeWidget:
    """
    Build cube edges to evaluate left ventricle relative position
    """
    def __init__(self):
        self._line_source = []  # 12 sides of cube
        self._line_actor = []
        self._line_mapper = []
        self._cube_renderer = None

        self._initialize_cube_lines()

    def _initialize_cube_lines(self):
        for i in range(12):
            self._line_source.append(vtk.vtkLineSource())

            self._line_mapper.append(vtk.vtkDataSetMapper())
            self._line_mapper[i].SetInputData(self._line_source[i].GetOutput())

            self._line_actor.append(vtk.vtkActor())
            self._line_actor[i].SetMapper(self._line_mapper[i])

    def set_side_size(self, side_size):
        for i in range(3):
            self._line_source[i].SetPoint1([0, 0, 0])
        self._line_source[0].SetPoint2([side_size, 0, 0])
        self._line_source[1].SetPoint2([0, side_size, 0])
        self._line_source[2].SetPoint2([0, 0, side_size])

        for i in range(3, 6):
            self._line_source[i].SetPoint1([side_size, side_size, side_size])
        self._line_source[3].SetPoint2([side_size, side_size, 0])
        self._line_source[4].SetPoint2([side_size, 0, side_size])
        self._line_source[5].SetPoint2([0, side_size, side_size])

        for i in range(6, 8):
            self._line_source[i].SetPoint1([0, side_size, side_size])
        self._line_source[6].SetPoint2([0, 0, side_size])
        self._line_source[7].SetPoint2([0, side_size, 0])

        for i in range(8, 10):
            self._line_source[i].SetPoint1([side_size, side_size, 0])
        self._line_source[8].SetPoint2([0, side_size, 0])
        self._line_source[9].SetPoint2([side_size, 0, 0])

        self._line_source[10].SetPoint1([side_size, 0, 0])
        self._line_source[10].SetPoint2([side_size, 0, side_size])

        self._line_source[11].SetPoint1([0, 0, side_size])
        self._line_source[11].SetPoint2([side_size, 0, side_size])

        for i in range(12):
            self._line_source[i].Update()

    def set_renderer(self, renderer):
        self._cube_renderer = renderer
        for i in range(12):
            self._cube_renderer.AddActor(self._line_actor[i])
