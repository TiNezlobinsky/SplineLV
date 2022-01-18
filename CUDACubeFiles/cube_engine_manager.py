from CUDACubeFiles.cube_generator.cube_generator import CubeGenerator


class CubeEngineManager:
    """
    Central class for the package controlling.
    Binds with CubeVisualizationWidget to provide it's methods
    for application management
    """
    def __init__(self):
        self._vtk_scene = None

        self._cube_generator = CubeGenerator()

        self._parameters_dict = {}

        self._cube_side_size = 256

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

    def _visualize_cube(self):
        self._vtk_scene.visualize_cube()

    def get_vtk_scene(self):
        """
        Get the vtk scene, which was connected

        Returns
        -------
        get_vtk_scene : VtkCubeScene object
        """
        return self._vtk_scene

    def set_cube_size(self, size):
        """
        Set cube side size (points)

        Parameters
        ----------
        size : int
            number of points in cube side
        """
        self._cube_side_size = size

    def set_parameters(self, parameters_dict):
        """
        Set parameters entered by user

        Parameters
        ----------
        parameters_dict : dict
        """
        self._cube_generator.set_parameters(parameters_dict)

    def set_data_dict(self, data_dict):
        """
        Set data from another package as input

        Parameters
        ----------
        data_dict : dict
            keys:
            mesh : vtk vertex with fibers
            surface : polygonal surfaces (epi, endo, base)
        """
        self._cube_generator.read_mesh(data_dict["mesh"])
        self._cube_generator.read_surface(data_dict["surface"])

    def generate(self):
        """
        Generate cube for input mesh and entered parameters
        """
        self._cube_generator.generate_cubes()
        self._cube_generator.construct_cube()
        self._vtk_scene.set_cube(self._cube_generator.get_cube())
        self._vtk_scene.set_cube_bounds(self._cube_side_size)

    def get_arrays(self):
        """
        Get cube array and and corresponding fibers as dict

        Returns
        -------
        get_arrays : dict
            keys:
            cube_array : numpy array
            fibers_array : numpy array
        """
        return {"cube_array": self._cube_generator.get_cube_array(),
                "fibers_array": self._cube_generator.get_fibers()}
