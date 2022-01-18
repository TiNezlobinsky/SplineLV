

class LocalStorage:
    """
    Store data and binds packages for data exchange.
    Works as a chain, but can be extended to a more complicated behaviour
    """
    def __init__(self):
        self._storage_dict = {}

        # Keys list:
        # "VarBaseMeasurement" - spline measurement package,
        # "Reconstruction"     - reconstruction package,
        # "CUDACubes"          - generate bin files for TNNP-CUDA software,
        # "DiffFibrosis"       - generate diff. fibrosis for TNNP-CUDA software

    def add_block(self, key_str):
        """
        Register a new package to store it's data

        Parameters
        ----------
        key_str : str
            Package registry key
        """
        self._storage_dict[key_str] = {}

    def get_access(self, key_str):
        """
        Get the data for corresponding package

        Parameters
        ----------
        key_str :
            Package registry key
        """
        if key_str == "Reconstruction":
            return self._storage_dict["VarBaseMeasurement"]
        elif key_str == "CUDACubes":
            return self._storage_dict["Reconstruction"]
        elif key_str == "DiffFibrosis":
            return self._storage_dict["CUDACubes"]

    def upload_data(self, block_str, data_dict):
        """
        Upload data for corresponding package

        Parameters
        ----------
        block_str : str
            Package registry key

        data_dict : dict
        """
        self._storage_dict[block_str] = data_dict

