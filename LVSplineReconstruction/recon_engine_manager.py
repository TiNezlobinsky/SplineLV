from LVSplineReconstruction.reconstruction.var_z_algorithm.var_z_reconstruction import VarZReconstruction
from LVSplineReconstruction.reconstruction.polygonal_surface_assembly import PolygonalSurfaceAssembly
import vtk
import fileinput
from LVSplineReconstruction.additions.decorators import check_initialization


# CODE REGIONS:
# 1) Scene visualization
# 2) Vertex mesh and fibers constructor
# 3) Polygon mesh constructors
# 4) Setters
# 5) Getters
# 6) Writers


class ReconEngineManager:
    """
    Central class for the package controlling.
    Binds with ReconstructionWidget to provide it's methods
    for application management
    """
    def __init__(self):
        self._vtk_scene = None

        self._var_z_reconstruction = VarZReconstruction()
        self._polygonal_surface_assembly = PolygonalSurfaceAssembly()

        self._data_dict = {}  # input data
        self._output_dict = {
            "mesh": None,
            "surface": {}
        }

    def connect_with_scene(self, vtk_scene):
        """
        Connect with the scene

        Parameters
        ----------
        vtk_scene : vtk object
            VtkScene class object
        """
        self._vtk_scene = vtk_scene

    def run_the_scene(self):
        """
        Run the scene. Initialize vtk window
        """
        self._vtk_scene.initialize_window()

# SCENE VISUALIZATION:

    @check_initialization
    def visualize_diff_mesh(self):
        """
        Display vertices mesh on the scene
        """
        self._vtk_scene.set_mesh(self._var_z_reconstruction.get_full_mesh())
        self._vtk_scene.reset_camera()

    @check_initialization
    def visualize_elem_surface(self):
        """
        Display polygonal mesh on the scene
        """
        self._vtk_scene.set_mesh(self._polygonal_surface_assembly.get_unstructured_grid())
        self._vtk_scene.reset_camera()

    @check_initialization
    def visualize_fibers(self):
        """
        Display fibers field (vectors) on the scene
        """
        self._vtk_scene.set_mesh(self._var_z_reconstruction.get_full_mesh(), fibers=True)
        self._vtk_scene.reset_camera()

# VERTEX MESH AND FIBERS CONSTRUCTOR:

    @check_initialization
    def construct_mesh(self):
        """
        Perform reconstruction with input data
        """
        self._var_z_reconstruction.reconstruct()
        self._output_dict["mesh"] = self._var_z_reconstruction.get_full_mesh()

# POLYGON MESH CONSTRUCTORS:

    @check_initialization
    def construct_polygonal_surfaces(self):
        """
        Build epi, endo, base surfaces and unite them in one polygonal mesh
        """
        self.assembly_epi_surface()
        self.assembly_endo_surface()
        self.assembly_base_surface()
        self._polygonal_surface_assembly.merge()

    def assembly_epi_surface(self):
        self._polygonal_surface_assembly.set_points(
            self._var_z_reconstruction.get_surfaces_dict()["epi"].GetPoints())
        self._polygonal_surface_assembly.set_dist_inc(7)
        self._polygonal_surface_assembly.set_tolerance(0.0001)
        self._polygonal_surface_assembly.set_dist_pow(2)
        self._polygonal_surface_assembly.assembly()
        self._output_dict["surface"]["epi"] = self._polygonal_surface_assembly.get_assembled_surface()
        self._polygonal_surface_assembly.add_assembled_surface_to_list()

    def assembly_endo_surface(self):
        self._polygonal_surface_assembly.set_points(
            self._var_z_reconstruction.get_surfaces_dict()["endo"].GetPoints())
        self._polygonal_surface_assembly.set_dist_inc(2)
        self._polygonal_surface_assembly.set_tolerance(0.0001)
        self._polygonal_surface_assembly.set_dist_pow(2)
        self._polygonal_surface_assembly.assembly()
        self._output_dict["surface"]["endo"] = self._polygonal_surface_assembly.get_assembled_surface()
        self._polygonal_surface_assembly.add_assembled_surface_to_list()

    def assembly_base_surface(self):
        polydata_with_border = vtk.vtkPolyData()
        cell_array = vtk.vtkCellArray()

        hole_endo_points = self._var_z_reconstruction.get_surfaces_dict()["hole_endo"].GetPoints()

        cell_array.InsertNextCell(hole_endo_points.GetNumberOfPoints())
        for i in range(hole_endo_points.GetNumberOfPoints())[::-1]:
            point = hole_endo_points.GetPoint(i)
            index = self._var_z_reconstruction.get_surfaces_dict()["base"].FindPoint(point)
            cell_array.InsertCellPoint(index)

        polydata_with_border.SetPoints(
            self._var_z_reconstruction.get_surfaces_dict()["base"].GetPoints())
        polydata_with_border.SetPolys(cell_array)

        self._polygonal_surface_assembly.set_points(
            self._var_z_reconstruction.get_surfaces_dict()["base"].GetPoints())
        self._polygonal_surface_assembly.set_dist_inc(2)
        self._polygonal_surface_assembly.set_tolerance(0)
        self._polygonal_surface_assembly.set_dist_pow(2)
        self._polygonal_surface_assembly.assembly_with_constrains(polydata_with_border)
        self._output_dict["surface"]["base"] = self._polygonal_surface_assembly.get_assembled_surface()
        self._polygonal_surface_assembly.add_assembled_surface_to_list()

# SETTERS:

    def set_data_dict(self, data_dict):
        """
        Set data dict as an input to reconstruction

        Parameters
        ----------
        data_dict : dict
            keys:
            meridians : dict
            common : dict
        """
        self._data_dict = data_dict
        self._var_z_reconstruction.set_data_dict(self._data_dict)

    def set_wall_points(self, points_num):
        """
        Set psi layers number

        Parameters
        ----------
        points_num : int
        """
        self._var_z_reconstruction.set_wall_points(points_num)

    def set_surface_points(self, points_num):
        """
        Set phi layers number

        Parameters
        ----------
        points_num : int
        """
        self._var_z_reconstruction.set_surfaces_points(points_num)

    def set_layers_number(self, layers_num):
        """
        Set gamma layers number

        Parameters
        ----------
        layers_num : int
        """
        self._var_z_reconstruction.set_gamma_layers(layers_num)

    def set_opacity(self, value):
        """
        Change an object transparency

        Parameters
        ----------
        value: float
            from 0 to 1.
        """
        self._vtk_scene.set_opacity(value)

    def set_gamma_1(self, gamma_1):
        """
        Set gamma1 to change fibers rotation angle

        Parameters
        ----------
        gamma_1 : float
        """
        self._var_z_reconstruction.set_gamma_1(gamma_1)

    def set_gamma_0(self, gamma_0):
        """
        Set gamma0 to change fibers rotation angle

        Parameters
        ----------
        gamma_0 : float
        """
        self._var_z_reconstruction.set_gamma_0(gamma_0)

# GETTERS:

    def get_vtk_scene(self):
        """
        Get the vtk scene, which was connected

        Returns
        -------
        get_vtk_scene : VtkMeasScene object
        """
        return self._vtk_scene

    def get_reconstructed(self):
        """
        Get the dict with reconstructed data

        Returns
        -------
        get_reconstructed : dict
            keys:
            mesh : vtkUnstructuredGrid with vectors
            surface : vtkPolyData
        """
        return self._output_dict

    def get_data_dict(self):
        """
        Get the input data

        Returns
        -------
        get_data_dict : dict
        """
        return self._data_dict

# WRITERS:

    @check_initialization
    def write_unstructured_grid(self):
        """
        Write vertices mesh with fibers to vtk file
        """
        writer = vtk.vtkUnstructuredGridWriter()
        writer.SetFileName("MeshwFibers.vtk")
        writer.SetInputData(self._var_z_reconstruction.get_full_mesh())
        writer.Write()
        self._file_correction("MeshwFibers.vtk")

    @check_initialization
    def write_polydata_grid(self):
        """
        Write lv polygonal surface to vtk file
        """
        writer = vtk.vtkPolyDataWriter()
        writer.SetFileName("LVSurfaces.vtk")
        writer.SetInputData(self._polygonal_surface_assembly.get_polydata())
        writer.Write()
        self._file_correction("LVSurfaces.vtk")

    def _file_correction(self, file_name):
        # when vtk file is writing (qt encoding?),
        # points are replaced by commas, and it does
        # not match the vtk file format
        try:
            for line in fileinput.input(file_name, inplace=True):
                print (line.replace(',', '.'),)  # , (comma) is needed to avoid blank lines
        except Exception:
            print (">>> Problem with file correction (Debug)")
