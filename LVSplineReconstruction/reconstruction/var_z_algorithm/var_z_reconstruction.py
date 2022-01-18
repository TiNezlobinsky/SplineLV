import vtk
import fileinput
from math import pi, sin, cos, sqrt
import numpy as np
from LVSplineReconstruction.reconstruction.var_z_algorithm.ro_psi_spline import RoPsiSpline
from LVSplineReconstruction.reconstruction.var_z_algorithm.z_phi_spline import ZPhiSpline
from LVSplineReconstruction.reconstruction.var_z_algorithm.ro_phi_spline import RoPhiSpline


# CODE REGIONS:
# 1) Splines initialization
# 2) Getters
# 3) Setters
# 4) Surface construction
# 5) Mesh and fibers construction


class VarZReconstruction:
    def __init__(self):
        self._data_dict = {}

        self._full_mesh = None
        self._surfaces_dict = {
            "epi": None,
            "endo": None,
            "base": None,
            "hole_endo": None,
            "hole_epi": None
        }
        self._surfaces_mesh = None

        self._gamma_1 = 1.
        self._gamma_0 = 0.

        self._psi_points_number = 100
        self._phi_points_number = 100
        self._gamma_layers_number = 10

        self._x_array_surface = np.array([])
        self._y_array_surface = np.array([])
        self._z_array_surface = np.array([])

        self._ro_psi_spline = RoPsiSpline()
        self._z_phi_spline = ZPhiSpline()
        self._ro_phi_spline = RoPhiSpline()
        self._ro_phi_spline_epi = RoPhiSpline()
        self._ro_phi_spline_endo = RoPhiSpline()
        self._ro_phi_spline_epi_1 = RoPhiSpline()
        self._ro_phi_spline_endo_1 = RoPhiSpline()

        self._meridians_number = 0

    def reconstruct(self):
        self.construct_surfaces()
        self.construct_mesh()

# SPLINES INITIALIZATION:

    def _initialize_splines(self):
        self._z_phi_spline.set_number_of_meridians(self._meridians_number)
        self._ro_phi_spline.set_number_of_meridians(self._meridians_number)
        self._ro_phi_spline_epi.set_number_of_meridians(self._meridians_number)
        self._ro_phi_spline_endo.set_number_of_meridians(self._meridians_number)
        self._ro_phi_spline_epi_1.set_number_of_meridians(self._meridians_number)
        self._ro_phi_spline_endo_1.set_number_of_meridians(self._meridians_number)

        self._ro_psi_spline.set_psi_intervals_points(self._psi_points_number)
        self._ro_phi_spline.set_phi_intervlals_points(self._phi_points_number)
        self._ro_phi_spline_endo.set_phi_intervlals_points(self._phi_points_number)
        self._ro_phi_spline_endo_1.set_phi_intervlals_points(self._phi_points_number)
        self._ro_phi_spline_epi.set_phi_intervlals_points(self._phi_points_number)
        self._ro_phi_spline_epi_1.set_phi_intervlals_points(self._phi_points_number)
        self._z_phi_spline.set_z_intervlals_points(self._phi_points_number)

# GETTERS:

    def get_full_mesh(self):
        return self._full_mesh

    def get_surfaces_mesh(self):
        return self._surfaces_mesh

    def get_surfaces_dict(self):
        return self._surfaces_dict

# SETTERS:

    def set_data_dict(self, data_dict):
        self._data_dict = data_dict

    def set_gamma_1(self, gamma_1):
        self._gamma_1 = gamma_1

    def set_gamma_0(self, gamma_0):
        self._gamma_0 = gamma_0

    def set_wall_points(self, points_num):
        self._psi_points_number = points_num

    def set_surfaces_points(self, points_num):
        self._phi_points_number = points_num

    def set_gamma_layers(self, layers_num):
        self._gamma_layers_number = layers_num

    def set_number_of_meridians(self, number):
        self._meridians_number = number

# SURFACE CONSTRUCTION:

    def construct_surfaces(self):
        self.set_number_of_meridians(len(self._data_dict["meridians"]))
        self._initialize_splines()
        surfaces_points_dict = {}
        surfaces_points_dict["epi"] = self.construct_lv_surface("epi", 0)
        surfaces_points_dict["endo"] = self.construct_lv_surface("endo", 1)
        surfaces_points_dict["base"] = self.construct_lv_base()
        surfaces_points_dict["hole_endo"] = self.construct_lv_hole(1)
        surfaces_points_dict["hole_epi"] = self.construct_lv_hole(0)

        self._surfaces_dict["epi"] = self._construct_vtk_mesh(surfaces_points_dict["epi"])
        self._surfaces_dict["endo"] = self._construct_vtk_mesh(surfaces_points_dict["endo"])
        self._surfaces_dict["base"] = self._construct_vtk_mesh(surfaces_points_dict["base"])
        self._surfaces_dict["hole_endo"] = self._construct_vtk_mesh(surfaces_points_dict["hole_endo"])
        self._surfaces_dict["hole_epi"] = self._construct_vtk_mesh(surfaces_points_dict["hole_epi"])

        combined_surfaces_points = self._combine_surfaces(surfaces_points_dict)
        self._surfaces_mesh = self._construct_vtk_mesh(combined_surfaces_points)

    def _combine_surfaces(self, surfaces_dict):
        x = np.array([])
        y = np.array([])
        z = np.array([])
        for surface_str in surfaces_dict:
            if surface_str == "hole":
                continue
            x = np.append(x, surfaces_dict[surface_str][0])
            y = np.append(y, surfaces_dict[surface_str][1])
            z = np.append(z, surfaces_dict[surface_str][2])

        return [x, y, z]

    def construct_lv_surface(self, layer, gamma):
        x_list = []
        y_list = []
        z_list = []

        z_coordinates = []
        ro_coordinates = []
        for meridian in self._data_dict["meridians"]:
            self._ro_psi_spline.set_coordiantes(meridian[layer]["ro"],
                                                meridian[layer]["z"])
            self._ro_psi_spline.set_gamma(gamma)
            self._ro_psi_spline.set_Zmax(meridian[layer]["Zmax"])
            self._ro_psi_spline.set_h(self._data_dict["common"]["h"])
            self._ro_psi_spline.compute()
            ro_coordinates.append(self._ro_psi_spline.get_ro_array())
            z_coordinates.append(self._ro_psi_spline.get_z_array())

        z_array = np.array(z_coordinates).T
        ro_array = np.array(ro_coordinates).T

        for z_level_list in z_array:
            self._z_phi_spline.set_z_list(z_level_list)
            self._z_phi_spline.compute()
            z_list.append(self._z_phi_spline.get_z_array())

        for ro_level_list in ro_array:
            self._ro_phi_spline.set_ro_list(ro_level_list)
            self._ro_phi_spline.compute()
            x_list.append(self._ro_phi_spline.get_x_array())
            y_list.append(self._ro_phi_spline.get_y_array())

        return [np.array(x_list).flatten(),
                np.array(y_list).flatten(),
                np.array(z_list).flatten()]

    def construct_lv_base(self):
        x_list = []
        y_list = []
        z_list = []

        ro_array_list = []
        ro_list_epi = []
        ro_list_endo = []

        zmax_list = []

        gamma_list = np.linspace(0, 1, self._gamma_layers_number)

        for meridian in self._data_dict["meridians"]:
            self._ro_psi_spline.set_coordiantes(meridian["epi"]["ro"],
                                                meridian["epi"]["z"])
            self._ro_psi_spline.set_gamma(self._gamma_0)
            self._ro_psi_spline.set_Zmax(meridian["epi"]["Zmax"])
            self._ro_psi_spline.set_h(self._data_dict["common"]["h"])
            self._ro_psi_spline.compute()
            ro_list_epi.append(self._ro_psi_spline.get_ro_array())

        for meridian in self._data_dict["meridians"]:
            self._ro_psi_spline.set_coordiantes(meridian["endo"]["ro"],
                                                meridian["endo"]["z"])
            self._ro_psi_spline.set_gamma(self._gamma_1)
            self._ro_psi_spline.set_Zmax(meridian["endo"]["Zmax"])
            self._ro_psi_spline.set_h(self._data_dict["common"]["h"])
            self._ro_psi_spline.compute()
            ro_list_endo.append(self._ro_psi_spline.get_ro_array())
            zmax_list.append(meridian["endo"]["Zmax"])

        h = self._data_dict["common"]["h"]

        ro_array_epi = list(np.array(ro_list_epi).T)
        ro_array_endo = list(np.array(ro_list_endo).T)

        psi = 0

        for gamma in gamma_list:
            self._ro_phi_spline_epi.set_ro_list(ro_array_epi[0])
            self._ro_phi_spline_epi.compute()
            self._ro_phi_spline_endo.set_ro_list(ro_array_endo[0])
            self._ro_phi_spline_endo.compute()
            ro_array_list.append(self._ro_phi_spline_epi.get_ro_array()*(1 - gamma) +
                                     self._ro_phi_spline_endo.get_ro_array()*gamma)

            x_list.append(ro_array_list[-1]*np.cos(self._ro_phi_spline_endo.get_phi_array()))
            y_list.append(ro_array_list[-1]*np.sin(self._ro_phi_spline_endo.get_phi_array()))

            z_mer_list = []
            for zmax in zmax_list:
                z_mer_list.append(zmax - (zmax - h*gamma)*sin(psi))
            self._z_phi_spline.set_z_list(z_mer_list)
            self._z_phi_spline.compute()
            z_list.append(self._z_phi_spline.get_z_array())

        return [np.array(x_list).flatten(),
                np.array(y_list).flatten(),
                np.array(z_list).flatten()]

    def construct_lv_hole(self, gamma):
        # to define hole and cut it in further
        x_list = []
        y_list = []
        z_list = []

        ro_array_list = []
        ro_list_epi = []
        ro_list_endo = []

        zmax_list = []

        gamma_list = [gamma, ]

        for meridian in self._data_dict["meridians"]:
            self._ro_psi_spline.set_coordiantes(meridian["epi"]["ro"],
                                                meridian["epi"]["z"])
            self._ro_psi_spline.set_gamma(self._gamma_0)
            self._ro_psi_spline.set_Zmax(meridian["epi"]["Zmax"])
            self._ro_psi_spline.set_h(self._data_dict["common"]["h"])
            self._ro_psi_spline.compute()
            ro_list_epi.append(self._ro_psi_spline.get_ro_array())

        for meridian in self._data_dict["meridians"]:
            self._ro_psi_spline.set_coordiantes(meridian["endo"]["ro"],
                                                meridian["endo"]["z"])
            self._ro_psi_spline.set_gamma(self._gamma_1)
            self._ro_psi_spline.set_Zmax(meridian["endo"]["Zmax"])
            self._ro_psi_spline.set_h(self._data_dict["common"]["h"])
            self._ro_psi_spline.compute()
            ro_list_endo.append(self._ro_psi_spline.get_ro_array())
            zmax_list.append(meridian["endo"]["Zmax"])

        h = self._data_dict["common"]["h"]

        ro_array_epi = list(np.array(ro_list_epi).T)
        ro_array_endo = list(np.array(ro_list_endo).T)

        psi = 0

        for gamma in gamma_list:
            self._ro_phi_spline_epi.set_ro_list(ro_array_epi[0])
            self._ro_phi_spline_epi.compute()
            self._ro_phi_spline_endo.set_ro_list(ro_array_endo[0])
            self._ro_phi_spline_endo.compute()
            ro_array_list.append(self._ro_phi_spline_epi.get_ro_array() * (1 - gamma) +
                                 self._ro_phi_spline_endo.get_ro_array() * gamma)

            x_list.append(ro_array_list[-1] * np.cos(self._ro_phi_spline_endo.get_phi_array()))
            y_list.append(ro_array_list[-1] * np.sin(self._ro_phi_spline_endo.get_phi_array()))

            z_mer_list = []
            for zmax in zmax_list:
                z_mer_list.append(zmax - (zmax - h * gamma) * sin(psi))
            self._z_phi_spline.set_z_list(z_mer_list)
            self._z_phi_spline.compute()
            z_list.append(self._z_phi_spline.get_z_array())

        return [np.array(x_list).flatten(),
                np.array(y_list).flatten(),
                np.array(z_list).flatten()]

# MESH AND FIBERS CONSTRUCTION:

    def construct_mesh(self):
        self.set_number_of_meridians(len(self._data_dict["meridians"]))
        self._initialize_splines()

        x_array_3d = []
        y_array_3d = []
        z_array_3d = []
        fibers_x_3d = []
        fibers_y_3d = []
        fibers_z_3d = []
        ro_array_3d = []
        ro_list_epi = []
        ro_list_endo = []

        zmax_list = []

        gamma_list = np.linspace(self._gamma_0, self._gamma_1, self._gamma_layers_number)

        for meridian in self._data_dict["meridians"]:
            self._ro_psi_spline.set_coordiantes(meridian["epi"]["ro"],
                                                meridian["epi"]["z"])
            self._ro_psi_spline.set_gamma(0)
            self._ro_psi_spline.set_Zmax(meridian["epi"]["Zmax"])
            self._ro_psi_spline.set_h(self._data_dict["common"]["h"])
            self._ro_psi_spline.compute()
            ro_list_epi.append(self._ro_psi_spline.get_ro_array())

        for meridian in self._data_dict["meridians"]:
            self._ro_psi_spline.set_coordiantes(meridian["endo"]["ro"],
                                                meridian["endo"]["z"])
            self._ro_psi_spline.set_gamma(1)
            self._ro_psi_spline.set_Zmax(meridian["endo"]["Zmax"])
            self._ro_psi_spline.set_h(self._data_dict["common"]["h"])
            self._ro_psi_spline.compute()
            ro_list_endo.append(self._ro_psi_spline.get_ro_array())
            zmax_list.append(meridian["endo"]["Zmax"])

        h = self._data_dict["common"]["h"]

        ro_array_epi = list(np.array(ro_list_epi).T)
        ro_array_endo = list(np.array(ro_list_endo).T)

        psi_array = np.linspace(0, (pi/2-0.0001), len(ro_array_endo))  # -0.0001 to prevent a value error

        for gamma in gamma_list:
            for i in range(len(ro_array_endo)):
                self._ro_phi_spline_epi.set_ro_list(ro_array_epi[i])
                self._ro_phi_spline_epi.compute()
                self._ro_phi_spline_endo.set_ro_list(ro_array_endo[i])
                self._ro_phi_spline_endo.compute()
                ro_array_3d.append(self._ro_phi_spline_epi.get_ro_array()*(1 - gamma) +
                                   self._ro_phi_spline_endo.get_ro_array()*gamma)

                x_array_3d.append(ro_array_3d[-1]*np.cos(self._ro_phi_spline_endo.get_phi_array()))
                y_array_3d.append(ro_array_3d[-1]*np.sin(self._ro_phi_spline_endo.get_phi_array()))

                z_mer_list = []
                for zmax in zmax_list:
                    z_mer_list.append(zmax - (zmax - h*gamma)*sin(psi_array[i]))
                self._z_phi_spline.set_z_list(z_mer_list)
                self._z_phi_spline.compute()
                z_array_3d.append(self._z_phi_spline.get_z_array())

                dr_dgam = self._ro_phi_spline_endo.get_ro_array() - self._ro_phi_spline_epi.get_ro_array()

                if i == len(ro_array_endo) - 1:
                    self._ro_phi_spline_epi_1.set_ro_list(ro_array_epi[i-1])
                    self._ro_phi_spline_epi_1.compute()
                    self._ro_phi_spline_endo_1.set_ro_list(ro_array_endo[i-1])
                    self._ro_phi_spline_endo_1.compute()
                else:
                    self._ro_phi_spline_epi_1.set_ro_list(ro_array_epi[i+1])
                    self._ro_phi_spline_epi_1.compute()
                    self._ro_phi_spline_endo_1.set_ro_list(ro_array_endo[i+1])
                    self._ro_phi_spline_endo_1.compute()

                dr_dpsi = ((self._ro_phi_spline_epi_1.get_ro_array()*(1 - gamma) +
                            self._ro_phi_spline_endo_1.get_ro_array()*gamma) -
                            (self._ro_phi_spline_epi.get_ro_array()*(1 - gamma) +
                            self._ro_phi_spline_endo.get_ro_array()*gamma))/(pi/2/self._psi_points_number)

                dr_dphi = ((self._ro_phi_spline_epi.get_ro_array()*(1 - gamma) +
                            self._ro_phi_spline_endo.get_ro_array()*gamma) -
                           (np.roll(self._ro_phi_spline_epi.get_ro_array(), 1)*(1 - gamma) +
                            np.roll(self._ro_phi_spline_endo.get_ro_array(), 1)*gamma))/(2*pi/self._phi_points_number)

                Ph = pi*gamma
                phi_max = 3*pi
                phi_array = self._ro_phi_spline_endo.get_phi_array()

                fibers_x_3d.append(sin(Ph)/((pi - 2*psi_array[i])*(self._gamma_1 - self._gamma_0)) *
                                         (y_array_3d[-1]*phi_max -
                                         (dr_dgam + dr_dphi*phi_max)*np.cos(phi_array)) -
                                         np.cos(phi_array)*dr_dpsi*pi/2*cos(Ph))
                fibers_y_3d.append(sin(Ph)/((2*psi_array[i] - pi)*(self._gamma_1 - self._gamma_0)) *
                                         (x_array_3d[-1]*phi_max -
                                         (dr_dgam + dr_dphi*phi_max)*np.sin(phi_array)) -
                                         np.sin(phi_array)*dr_dpsi*pi/2*cos(Ph))
                fibers_z_3d.append((h*sin(Ph)*np.sin(psi_array[i]))/((2*psi_array[i] - pi) *
                                         (self._gamma_1 - self._gamma_0)) +
                                         (np.array(z_array_3d[0]) - h*gamma) *
                                         np.cos(psi_array[i])*pi/2*cos(Ph))

        points_z = np.array(z_array_3d).flatten()
        points_x = np.array(x_array_3d).flatten()
        points_y = np.array(y_array_3d).flatten()

        vx_array_3d = np.array(fibers_x_3d).flatten()
        vy_array_3d = np.array(fibers_y_3d).flatten()
        vz_array_3d = np.array(fibers_z_3d).flatten()

        self._full_mesh = self._construct_vtk_mesh([points_x, points_y, points_z],
                                                   [vx_array_3d, vy_array_3d, vz_array_3d])

    def _construct_vtk_mesh(self, points, fibers=None):
        vtk_mesh = vtk.vtkUnstructuredGrid()
        vtk_points = vtk.vtkPoints()

        if fibers:
            fibers_array = vtk.vtkDoubleArray()
            fibers_array.SetNumberOfComponents(3)
            fibers_array.SetName("Fibers")

        for i in range(len(points[0])):
            vtk_points.InsertPoint(i, points[0][i],
                                   points[1][i],
                                   points[2][i])
            vertex = vtk.vtkVertex()
            vertex.GetPointIds().SetId(0, i)
            vtk_mesh.InsertNextCell(vertex.GetCellType(), vertex.GetPointIds())

            if fibers:
                fibers_array.InsertNextTuple3(*self.norm_vector([fibers[0][i], fibers[1][i], fibers[2][i]]))

        vtk_mesh.SetPoints(vtk_points)

        if fibers:
            vtk_mesh.GetPointData().SetVectors(fibers_array)

        return vtk_mesh

    @staticmethod
    def norm_vector(vector):
        sum = sqrt(vector[0]**2 + vector[1]**2 + vector[2]**2)
        return [vector[0]/sum, vector[1]/sum, vector[2]/sum]
