from numpy import linspace
from scipy import interpolate
from math import pi
import numpy as np


class ZPhiSpline:
    """
    Translation psi coordinate to z coordinate (var base algorithm feature) by the periodic spline interpolation
    """

    def __init__(self):
        self._z_list = []
        self._phi_list = []
        self._z_array_1d = []
        self._phi_array = []

        self._z_interval_points = 100  # default interpolated points number

    def set_z_list(self, z_list):
        """
        Set z coordinates as the spline nodes to build the spline

        Parameters
        ----------
        ro_list : list
        """
        self._z_list = z_list
        self._z_list = np.append(self._z_list, self._z_list[0])

    def set_number_of_meridians(self, n):
        """
        Set the number of meridians to get a phi list to build the spline
        and compute z coordinates in those phi

        Parameters
        ----------
        n : int
        """
        self._phi_list = [i*(2*pi/n) for i in range(n)]
        self._phi_list.append(2*pi)

    def set_z_intervlals_points(self, points_num):
        """
        Set an interpolated points number

        Parameters
        ----------
        points_num : int
        """
        self._z_interval_points = points_num

    def get_z_array(self):
        """
        Get a numpy array with z coordinates

        Returns
        ----------
        get_z_array : numpy array
        """
        return self._z_array_1d

    def get_phi_array(self):
        """
        Get a numpy array with phi coordinates

        Returns
        ----------
        get_phi_array : numpy array
        """
        return self._phi_array

    def _compute_z_phi_spline(self):
        phi_0 = 0.
        phi_1 = 2*pi

        phi_array = linspace(phi_0, phi_1, self._z_interval_points)

        self._tck = interpolate.splrep(self._phi_list, self._z_list, s=0, per=True)  # for b-spline
        output_z = interpolate.splev(phi_array, self._tck)

        self._z_array_1d = output_z
        self._phi_array = phi_array

    def compute(self):
        """
        Compute spline with the set z coordinates and for set number of meridians
        """
        self._compute_z_phi_spline()
