import vtk
import numpy as np
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from .vtk_widget.cube_widget import CubeWidget


class VtkCubeScene(QVTKRenderWindowInteractor):
    def __init__(self, parent=None):
        QVTKRenderWindowInteractor.__init__(self, parent)
        
        self._cube = vtk.vtkUnstructuredGrid()
        self._cube_mapper = vtk.vtkDataSetMapper()
        self._cube_actor = vtk.vtkActor()

        self._cube_widget = CubeWidget()

    def _initialize_scene(self):
        self._cube_actor.SetMapper(self._cube_mapper)
        self._renderer.RemoveAllViewProps()
        self._renderer.AddActor(self._cube_actor)

        self._cube_widget.set_renderer(self._renderer)

    def initialize_window(self):
        self._renderer = vtk.vtkRenderer()
        self.GetRenderWindow().AddRenderer(self._renderer)
        self._interactor = self.GetRenderWindow().GetInteractor()
        self._interactor.SetInteractorStyle(vtk.vtkInteractorStyleTrackballCamera())
        self._interactor.Initialize()

        self._initialize_scene()

    def set_cube(self, cube_vtk_mesh):
        """
        Set cube representation object

        Parameters
        ----------
        cube_vtk_mesh : vtkUnstructuredGrid
        """
        self._cube = cube_vtk_mesh
        self._cube_mapper.SetInputData(self._cube)

        self._interactor.Initialize()

    def set_cube_bounds(self, size):
        """
        Set cube edges size (represents as lines)

        Parameters
        ----------
        size : int
        """
        self._cube_widget.set_side_size(size)
        self._interactor.Initialize()
