import vtk


class PolygonalSurfaceAssembly:
    def __init__(self):
        self._original_points = None
        self._output_polydata = None
        self._output_unstructured_grid = None
        self._current_polydata = None

        self._tolerance = 0

        self._dist_pow = 1
        self._dist_inc = 0

        self._append_filter = vtk.vtkAppendFilter()
        self._assembled_surface_list = []

    def set_points(self, points):
        """
        Set points set to construct polygonal mesh

        Parameters
        ----------
        points: points set vtk object
        """
        self._original_points = points
        self._current_polydata = vtk.vtkPolyData()

    def set_tolerance(self, tolerance):
        """
        Set tolerance for Delaunay2d algorithm

        Parameters
        ----------
        tolerance: float
        """
        self._tolerance = tolerance

    def set_dist_pow(self, pow_):
        """
        Set pow to expression for ... before triangulation:
            (y + increment ** 2) ** pow

        Parameters
        ----------
        pow_: float
        """
        self._dist_pow = pow_

    def set_dist_inc(self, inc):
        """
        Set increment to expression for ... before triangulation:
            (y + increment ** 2) ** pow

        Parameters
        ----------
        inc: float
        """
        self._dist_inc = inc

    def get_assembled_surface(self):
        # returns polydata
        return self._current_polydata

    def get_unstructured_grid(self):
        # merged grid
        return self._output_unstructured_grid

    def get_polydata(self):
        # merged polydata
        return self._output_polydata

    def add_assembled_surface_to_list(self):
        self._assembled_surface_list.append(self._current_polydata)

    def clear_assembled_list(self):
        self._assembled_surface_list = []

    def merge(self):
        for surface in self._assembled_surface_list:
            self._append_filter.AddInputData(surface)

        self._append_filter.Update()
        self._output_unstructured_grid = self._append_filter.GetOutput()
        self._convert_to_polydata()

        for surface in self._assembled_surface_list:
            self._append_filter.RemoveInputData(surface)

        self.clear_assembled_list()

    def _convert_to_polydata(self):
        geometry_filter = vtk.vtkGeometryFilter()
        geometry_filter.SetInputData(self._output_unstructured_grid)
        geometry_filter.Update()
        self._output_polydata = geometry_filter.GetOutput()

    def _distribute_points_in_2D(self):
        points_2d = vtk.vtkPoints()
        points_2d.DeepCopy(self._original_points)

        points_num = points_2d.GetNumberOfPoints()
        for i in range(points_num):
            point = self._original_points.GetPoint(i)
            # some expression for points distribution:
            coeff = (point[2] + self._dist_inc ** 2) ** self._dist_pow
            points_2d.SetPoint(i, coeff * point[0], coeff * point[1], 0)
        self._current_polydata.SetPoints(points_2d)

    def assembly(self):
        self._distribute_points_in_2D()

        delaunay_2d = vtk.vtkDelaunay2D()
        delaunay_2d.SetInputData(self._current_polydata)
        delaunay_2d.SetTolerance(self._tolerance)
        delaunay_2d.SetSourceData(self._current_polydata)
        delaunay_2d.Update()
        self._current_polydata = delaunay_2d.GetOutput()
        self._current_polydata.SetPoints(self._original_points)

    def assembly_with_constrains(self, polydata_with_border):
        self._distribute_points_in_2D()

        delaunay_2d = vtk.vtkDelaunay2D()
        delaunay_2d.SetInputData(polydata_with_border)
        delaunay_2d.SetTolerance(self._tolerance)
        delaunay_2d.SetSourceData(polydata_with_border)
        delaunay_2d.Update()

        self._current_polydata = delaunay_2d.GetOutput()
        self._current_polydata.SetPoints(self._original_points)

