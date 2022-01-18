import vtk
import numpy as np
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor


class VtkReconstructionScene(QVTKRenderWindowInteractor):
    def __init__(self, parent=None):
        QVTKRenderWindowInteractor.__init__(self, parent)

        self._mesh = vtk.vtkUnstructuredGrid()
        self._mesh_mapper = vtk.vtkDataSetMapper()
        self._mesh_actor = vtk.vtkActor()
        self._mesh_actor.SetMapper(self._mesh_mapper)

        self._fibers = vtk.vtkGlyph3D()
        self._fibers_representation = vtk.vtkArrowSource()
        self._fibers_representation.Update()
        self._fibers.SetSourceData(self._fibers_representation.GetOutput())
        self._fibers_mapper = vtk.vtkDataSetMapper()
        self._fibers_actor = vtk.vtkActor()
        self._fibers_actor.SetMapper(self._fibers_mapper)

    def initialize_window(self):
        self._renderer = vtk.vtkRenderer()
        self.GetRenderWindow().AddRenderer(self._renderer)
        self._interactor = self.GetRenderWindow().GetInteractor()
        self._interactor.SetInteractorStyle(vtk.vtkInteractorStyleTrackballCamera())
        self._interactor.Initialize()

    def set_mesh(self, vtk_mesh, fibers=False):
        """
        Set unstructured grid to display on the scene.

        Parameters
        ----------
        vtk_mesh : Unstructured grid vtk object
            Mesh to display

        fibers: bool
            To display vectors inplace of the elements of vtk_mesh if True
        """

        self._renderer.RemoveAllViewProps()
        self._mesh = vtk_mesh
        if fibers:
            self._fibers.SetInputData(self._mesh)
            self._fibers.Update()
            self._fibers_mapper.SetInputData(self._fibers.GetOutput())
            self._fibers.SetVectorModeToUseVector()
            self._fibers.SetScaleFactor(5)
            self._renderer.AddActor(self._fibers_actor)
        else:
            self._mesh_mapper.SetInputData(self._mesh)
            self._renderer.AddActor(self._mesh_actor)
        self._interactor.Initialize()

    def set_opacity(self, value):
        """
        Change an object transparency

        Parameters
        ----------
        value: float
            from 0 to 1.
        """

        self._mesh_actor.GetProperty().SetOpacity(value)
        self._interactor.Initialize()
