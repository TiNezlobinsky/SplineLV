import numpy as np
from numpy import linspace
from scipy import interpolate
from math import pi, asin, sin


class RoPsiSpline:
    """
    Epi- and endocardium contour by the spline interpolation on each slices
    """

    def __init__(self):
        self._ro_list = []
        self._z_list = []
        self._psi_list = []
        self._ro_array_1d = []
        self._psi_array = []
        self._z_array_1d = []

        self._Zmax = 0.
        self._h = 0.
        self._gamma = 0.

        self._psi_interval_points = 100  # default interpolated points number

    def set_coordiantes(self, ro_list, z_list):
        """
        Set (ro, z) coordinates as the spline nodes to build the spline

        Parameters
        ----------
        ro_list : list

        z_list: list
        """
        self._ro_list = ro_list
        self._z_list = z_list

    def set_Zmax(self, Zmax):
        """
        Set max Z value for the current meridian

        Parameters
        ----------
        Zmax : float
        """
        self._Zmax = Zmax

    def set_h(self, h):
        """
        Set h value (common for all meridians)

        Parameters
        ----------
        h : float
        """
        self._h = h

    def set_gamma(self, gamma):
        """
        Set gamma to define an epicardium or endocardium wall

        Parameters
        ----------
        gamma : float
        """
        self._gamma = gamma

    def set_psi_intervals_points(self, points_num):
        """
        Set an interpolated points number

        Parameters
        ----------
        points_num : int
        """
        self._psi_interval_points = points_num

    def get_ro_array(self):
        """
        Get a numpy array with interpolated ro coordinates

        Returns
        ----------
        get_ro_array : numpy array
        """
        return self._ro_array_1d

    def get_z_array(self):
        """
        Get a numpy array with computed z coordinates

        Returns
        ----------
        get_z_array : numpy array
        """
        return self._z_array_1d

    def get_psi_array(self):
        """
        Get a numpy array with psi coordinates

        Returns
        ----------
        get_psi_array : numpy array
        """
        return self._psi_array

    def _compute_ro_psi_spline(self):
        psi_0 = 0.
        psi_1 = pi/2

        psi_array = linspace(psi_0, psi_1, self._psi_interval_points)

        self._tck = interpolate.splrep(self._psi_list, self._ro_list, s=0)  # for b-spline
        output_ro = interpolate.splev(psi_array, self._tck)

        self._interpolate = interpolate.splev

        self._ro_array_1d = output_ro
        self._psi_array = psi_array

    def _compute_psi(self):
        self._psi_list = []
        for z in self._z_list:
            arg = (self._Zmax - z) / (self._Zmax - self._h*self._gamma)
            # To prevent domain error:
            if arg > 1.0:
                arg = 1.0
            psi = asin(arg)
            self._psi_list.append(psi)

    def _compute_z(self):
        self._z_array_1d = (self._Zmax - (self._Zmax - self._h*self._gamma)*np.sin(self._psi_array))

    def compute(self):
        """
        Compute spline with the set ro and z coordinates
        """
        self._compute_psi()
        self._compute_ro_psi_spline()
        self._compute_z()

