import vtk
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor


class VtkDiffFibrosisScene(QVTKRenderWindowInteractor):
    def __init__(self, parent=None):
        QVTKRenderWindowInteractor.__init__(self, parent)

        self._lv_cube = vtk.vtkUnstructuredGrid()
        self._lv_cube_mapper = vtk.vtkDataSetMapper()
        self._lv_cube_actor = vtk.vtkActor()

    def initialize_window(self):
        self._renderer = vtk.vtkRenderer()
        self.GetRenderWindow().AddRenderer(self._renderer)
        self._interactor = self.GetRenderWindow().GetInteractor()
        self._interactor.SetInteractorStyle(vtk.vtkInteractorStyleTrackballCamera())
        self._interactor.Initialize()

        self._initialize_scene()

    def set_lv_cube(self, cube_vtk_mesh):
        """
        Set the left ventricle mesh (in cube representation)

        Parameters
        ----------
        cube_vtk_mesh : vtkUnstructuredGrid object
        """
        self._lv_cube = cube_vtk_mesh
        self._lv_cube_mapper.SetInputData(self._lv_cube)

        self._interactor.Initialize()

    def _initialize_scene(self):
        self._lv_cube_actor.SetMapper(self._lv_cube_mapper)
        self._renderer.RemoveAllViewProps()
        self._renderer.AddActor(self._lv_cube_actor)
