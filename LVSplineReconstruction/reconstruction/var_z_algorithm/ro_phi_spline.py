import numpy as np
from numpy import linspace
from scipy import interpolate
from math import pi


class RoPhiSpline:
    """
    Epi- and endocardium surfaces construction by the periodic spline interpolation
    """

    def __init__(self):
        self._ro_list = []
        self._phi_list = []
        self._ro_array_1d = []
        self._phi_array = []
        self._x_array_2d = []
        self._y_array_2d = []

        self._phi_interval_points = 100  # default interpolated points number

    def set_ro_list(self, ro_list):
        """
        Set ro coordinates as the spline nodes to build the spline

        Parameters
        ----------
        ro_list : list
        """
        self._ro_list = ro_list
        self._ro_list = np.append(self._ro_list, self._ro_list[0])

    def set_number_of_meridians(self, n):
        """
        Set the number of meridians to get a phi list to build the spline
        and compute ro coordinates in those phi

        Parameters
        ----------
        n : int
        """
        self._phi_list = [i*(2*pi/n) for i in range(n)]
        self._phi_list.append(2*pi)

    def set_phi_intervlals_points(self, points_num):
        """
        Set an interpolated points number

        Parameters
        ----------
        points_num : int
        """
        self._phi_interval_points = points_num

    def get_ro_array(self):
        """
        Get a numpy array with ro coordinates

        Returns
        ----------
        get_ro_array : numpy array
        """
        return self._ro_array_1d

    def get_phi_array(self):
        """
        Get a numpy array with phi coordinates

        Returns
        ----------
        get_phi_array : numpy array
        """
        return self._phi_array

    def get_x_array(self):
        """
        Get a numpy array with x coordinates

        Returns
        ----------
        get_x_array : numpy array
        """
        return self._x_array_2d

    def get_y_array(self):
        """
        Get a numpy array with y coordinates

        Returns
        ----------
        get_y_array : numpy array
        """
        return self._y_array_2d

    def _compute_ro_phi_spline(self):
        phi_0 = 0.
        phi_1 = 2*pi

        phi_array = linspace(phi_0, phi_1, self._phi_interval_points)

        self._tck = interpolate.splrep(self._phi_list, self._ro_list, s=0, per=True)  # for b-spline
        output_ro = interpolate.splev(phi_array, self._tck)

        self._interpolate = interpolate.splev

        self._ro_array_1d = output_ro
        self._phi_array = phi_array

    def _compute_x_y(self):
        # represent in Cartesian coordinates (from Cylindrical)
        self._x_array_2d = np.array(self._ro_array_1d)*np.cos(np.array(self._phi_array))
        self._y_array_2d = np.array(self._ro_array_1d)*np.sin(np.array(self._phi_array))

    def compute(self):
        """
        Compute spline with the set ro coordinates and for set number of meridians
        """
        self._compute_ro_phi_spline()
        self._compute_x_y()

