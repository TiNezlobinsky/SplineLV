import vtk
from math import sqrt, degrees
import struct
import numpy as np


class CubeGenerator:
    """
    Build cube and insert left ventricle model in it.
    Point belonging based on left ventricle surface polygons normals directions.
    See self._in_LV method
    """
    def __init__(self):

        self._mesh = vtk.vtkUnstructuredGrid()
        self._mesh_vectors = None

        self._cube = None

        self._surface = {
            "epi": vtk.vtkPolyData(),
            "endo": vtk.vtkPolyData(),
            "base": vtk.vtkPolyData()
        }

        self._cube_array = np.array([])
        self._fibers_array = np.array([])

        self._parameters_dict = {}
        # parameters_dict:
        # "n_side"
        # "x0cube"
        # "y0cube"
        # "z0cube"
        # "dr"

        self._point_locator_epi = vtk.vtkPointLocator()
        self._point_locator_endo = vtk.vtkPointLocator()
        self._point_locator_base = vtk.vtkPointLocator()

        self._find_angle = vtk.vtkMath.AngleBetweenVectors
        self._subtract_vec = vtk.vtkMath.Subtract
        self._norm_vec = vtk.vtkMath.Normalize

        self._SCALE_CHAR = 127.0

    def read_mesh(self, vtk_mesh):
        self._mesh = vtk_mesh
        self._mesh_vectors = self._mesh.GetPointData().GetVectors()  # fibers

    def read_surface(self, surface):
        self._surface = surface

    def generate_cubes(self):
        """
        Build cube for input mesh ang generate a binary files
        """
        # should be faster
        n_side = self._parameters_dict["n_side"]
        x0cube = self._parameters_dict["x0cube"]
        y0cube = self._parameters_dict["y0cube"]
        z0cube = self._parameters_dict["z0cube"]
        dr = self._parameters_dict["dr"]

        self._cube_array = np.zeros([n_side, n_side, n_side], dtype="int8")
        self._fibers_array = np.zeros([3, n_side, n_side, n_side], dtype=str)

        self.compute_normals(self._surface["epi"], "epi")
        self.compute_normals(self._surface["endo"], "endo")
        self.compute_normals(self._surface["base"], "base")

        self._point_locator_epi.SetDataSet(self._surface["epi"])
        self._point_locator_epi.Update()
        self._point_locator_endo.SetDataSet(self._surface["endo"])
        self._point_locator_endo.Update()
        self._point_locator_base.SetDataSet(self._surface["base"])
        self._point_locator_base.Update()

        for i in range(n_side):
            for j in range(n_side):
                for k in range(n_side):
                    point = [x0cube+dr*i,
                             y0cube+dr*j,
                             z0cube+dr*k]
                    if self._in_LV(point, j):
                        self._cube_array[i][j][k] = 1
                        point_id = self._mesh.FindPoint(point)
                        vec = self._mesh_vectors.GetTuple(point_id)
                        self._fibers_array[0][i][j][k] = self._float_to_char(vec[0])
                        self._fibers_array[1][i][j][k] = self._float_to_char(vec[1])
                        self._fibers_array[2][i][j][k] = self._float_to_char(vec[2])
                    else:
                        self._fibers_array[0][i][j][k] = self._float_to_char(0)
                        self._fibers_array[1][i][j][k] = self._float_to_char(0)
                        self._fibers_array[2][i][j][k] = self._float_to_char(0)
            print (i)

        self.write_cube_points("heart.bin")
        self.write_fibers_angles("fibers.bin")

    def _in_LV(self, point):
        epi_id = self._point_locator_epi.FindClosestPoint(point)
        endo_id = self._point_locator_endo.FindClosestPoint(point)
        base_id = self._point_locator_base.FindClosestPoint(point)

        vec_to_point_epi = [0, 0, 0]
        vec_to_point_endo = [0, 0, 0]
        vec_to_point_base = [0, 0, 0]
        self._subtract_vec(point, self._surface["epi"].GetPoints().GetPoint(epi_id), vec_to_point_epi)
        self._subtract_vec(point, self._surface["endo"].GetPoints().GetPoint(endo_id), vec_to_point_endo)
        self._subtract_vec(point, self._surface["base"].GetPoints().GetPoint(base_id), vec_to_point_base)

        self._norm_vec(vec_to_point_epi)
        self._norm_vec(vec_to_point_endo)
        self._norm_vec(vec_to_point_base)

        norm_epi = self._surface["epi"].GetPointData().GetVectors().GetTuple(epi_id)
        norm_endo = self._surface["endo"].GetPointData().GetVectors().GetTuple(endo_id)
        norm_base = self._surface["base"].GetPointData().GetVectors().GetTuple(base_id)
        angle_epi = degrees(self._find_angle(norm_epi, vec_to_point_epi))
        angle_endo = degrees(self._find_angle(norm_endo, vec_to_point_endo))
        angle_base = degrees(self._find_angle(norm_base, vec_to_point_base))

        if abs(angle_epi) > 90:
            return False
        if abs(angle_endo) > 90:
            return False
        if abs(angle_base) > 90:
            return False

        return True

    def write_cube_points(self, file_name):
        """
        Write binary files needed for TNNP-CUDA program

        Parameters
        ----------
        file_name : str
        """
        char_array = np.where(self._cube_array, chr(1), chr(0))
        char_array.tofile(file_name)

    def write_fibers_angles(self, file_name):
        """
        Write binary files needed for TNNP-CUDA program

        Parameters
        ----------
        file_name : str
        """
        self._fibers_array.tofile(file_name)

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
                    if self._cube_array[i][j][k]:
                        points.InsertPoint(ii, i, j, k)
                        vertex = vtk.vtkVertex()
                        vertex.GetPointIds().SetId(0, ii)
                        self._cube.InsertNextCell(vertex.GetCellType(), vertex.GetPointIds())
                        ii += 1

        self._cube.SetPoints(points)

    def set_parameters(self, parameters_dict):
        """
        Set parameters entered by user

        Parameters
        ----------
        parameters_dict : dict
        """
        self._parameters_dict = parameters_dict

    def get_cube(self):
        """
        Get vtk object represented cube

        Returns
        -------
        get_cube : vtkUnstructuredGrid
            with elements - vertices
        """
        return self._cube

    def get_cube_array(self):
        """
        Get cube array

        Returns
        -------
        get_cube_array : numpy array
        """
        return self._cube_array

    def get_fibers(self):
        """
        Get fibers array

        Returns
        -------
        get_fibers : numpy array
        """
        return self._fibers_array

    def _float_to_char(self, value):
        return struct.pack("b", (int(value*self._SCALE_CHAR + 0.5)))  # magic for TNNP-CUDA program

    def compute_normals(self, polydata, surface_type):
        """
        Compute normals for the left ventricle surface polygons

        Parameters
        ----------
        polydata : vtkPolyData

        surface_type : endo, epi or base
        """
        polydata_normals = vtk.vtkPolyDataNormals()
        polydata_normals.SetInputData(polydata)
        polydata_normals.ComputeCellNormalsOn()
        # polydata_normals.ConsistencyOff()
        polydata_normals.SplittingOff()
        if surface_type == "endo":
            polydata_normals.FlipNormalsOn()
        elif surface_type == "base":
            polydata_normals.FlipNormalsOn()
        polydata_normals.Update()

        normals_array = vtk.vtkDoubleArray()
        normals_array.SetNumberOfComponents(3)
        normals_array.SetName("NormalVectors")

        original_array = polydata_normals.GetOutput().GetPointData().GetArray("Normals")

        for i in range(polydata_normals.GetOutput().GetPoints().GetNumberOfPoints()):
            normals_array.InsertNextTuple3(*original_array.GetTuple(i))

        polydata.GetPointData().SetVectors(normals_array)
