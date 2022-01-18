import vtk
import struct
import numpy as np


class FibrosisIntegrator:
    def __init__(self):

        self._cube = vtk.vtkUnstructuredGrid()

        self._cube_array = np.array([])
        self._fibers_array = np.array([])

        self._SCALE_CHAR = 127.0

    def set_cube_array(self, cube_array):
        """

        Parameters
        ----------
        cube_array : numpy array
        """
        self._cube_array = cube_array

    def set_fibers_array(self, fibers_array):
        """

        Parameters
        ----------
        fibers_array : numpy array
        """
        self._fibers_array = fibers_array

    def embed_uniform_points_fibrosis(self, percent):
        mask = np.random.rand(*self._cube_array.shape) <= percent/100.
        self._cube_array[np.logical_and(mask, self._cube_array)] = 2  # 0 - no tissue, 1 - normal, 2 - fibrosis
        self._fibers_array[:, mask] = self._float_to_char(0)

        self.write_bin_files()

    def construct_cube(self):
        """
        Build left ventricle in cube as vtkUnstructuredGrid to represent on the scene
        """
        self._cube = vtk.vtkUnstructuredGrid()

        points = vtk.vtkPoints()

        cube_side = len(self._cube_array)

        ii = 0
        for i in range(cube_side):
            for j in range(cube_side):
                for k in range(cube_side):
                    if self._cube_array[i][j][k] == 1:
                        points.InsertPoint(ii, i, j, k)
                        vertex = vtk.vtkVertex()
                        vertex.GetPointIds().SetId(0, ii)
                        self._cube.InsertNextCell(vertex.GetCellType(), vertex.GetPointIds())
                        ii += 1

        self._cube.SetPoints(points)

    def get_cube(self):
        return self._cube

    def _float_to_char(self, value):
        return struct.pack("b", (int(value*self._SCALE_CHAR + 0.5)))  # magic for TNNP-CUDA program

    def write_cube_points(self, file_name):
        """
        Write binary files needed for TNNP-CUDA program

        Parameters
        ----------
        file_name : str
        """
        char_array = np.where(self._cube_array == 1, chr(1), chr(0))
        char_array.tofile(file_name)

    def write_fibers_angles(self, file_name):
        """
        Write binary files needed for TNNP-CUDA program

        Parameters
        ----------
        file_name : str
        """
        self._fibers_array.tofile(file_name)

    def write_bin_files(self):
        self.write_cube_points("heart.bin")
        self.write_fibers_angles("fibers.bin")
