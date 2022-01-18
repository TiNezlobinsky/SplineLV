from DiffuseFibrosis.fibrosis.fibrosis_integrator import FibrosisIntegrator


class DiffFibrosisEngineManager:
    def __init__(self):
        self._vtk_scene = None

        self._fibrosis_integrator = FibrosisIntegrator()

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

    def get_vtk_scene(self):
        """
        Get the vtk scene, which was connected

        Returns
        -------
        get_vtk_scene : VtkCubeScene object
        """
        return self._vtk_scene

    def set_data_dict(self, data_dict):
        """
        Set data from another package as input

        Parameters
        ----------
        data_dict : dict
            keys:
            cube_array : numpy array
            fibers_array : numpy array
        """
        self._fibrosis_integrator.set_cube_array(data_dict["cube_array"])
        self._fibrosis_integrator.set_fibers_array(data_dict["fibers_array"])

    def embed_uniform_points_fibrosis(self, percent):
        """
        Set percent of fibrosis in the left ventricle model

        Parameters
        ----------
        percent : float
        """
        self._fibrosis_integrator.embed_uniform_points_fibrosis(percent)
        self._fibrosis_integrator.construct_cube()
        self._vtk_scene.set_lv_cube(self._fibrosis_integrator.get_cube())
