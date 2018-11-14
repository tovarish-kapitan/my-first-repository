import sys
import math
import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate
from mpl_toolkits.mplot3d import Axes3D
from bs4 import BeautifulSoup
from mayavi.mlab import *

import misc

class RadarSceneData:
    def __init__(self, our_kml_file):
        self.xradar_names = []
        self.xradar_positions = []
        self.lradar_names = []
        self.lradar_positions = []
        self.target_names = []
        self.target_trajectories = []
        self.approx_target_trajectories =[]
        self.long_slice_list = []
        self.lat_slice_list = []
        self.alt_slice_list = []
        
        with open (our_kml_file, encoding="UTF-8") as kml:
            my_kml = BeautifulSoup(kml, features="lxml")

        cake = my_kml.find("placemark")
        if cake == None:
            print("There is no Placemark tags in the file")
        else:
            while cake != None:
                name = cake.find("name").get_text()
                coord = cake.find("coordinates").get_text()
                coord = coord[5:-5]  #обрезаем знаки \t \n по краям и пробел в конце
                c_list = coord.split(' ')
                i = 0
                while i < len(c_list):
                    c_list[i] = c_list[i].split(',')
                    j = 0
                    while j < len(c_list[i]):
                        c_list[i][j] = float(c_list[i][j]) #все числовые строки переводим во float
                        j = j + 1
                    i = i + 1
                if name[0] == 'X':
                    long = cake.find("longitude").get_text()
                    lat = cake.find("latitude").get_text()
                    alt = cake.find("altitude").get_text()
                    self.xradar_names.append(name)
                    self.xradar_positions.append((float(long),float(lat),float(alt)))
                elif name[0] == 'L':
                    long = cake.find("longitude").get_text() 
                    lat = cake.find("latitude").get_text()
                    alt = cake.find("altitude").get_text()
                    self.lradar_names.append(name)
                    self.lradar_positions.append((float(long),float(lat),float(alt)))
                else:
                    self.target_names.append(name)
                    self.target_trajectories.append(c_list)
                my_kml.placemark.decompose()
                cake = my_kml.find("placemark")

    def traject_approx(self, dx=0.1):  #разбивает отрезки между точками траектории с шагом не более чем dx
        #и готовит координатные срезы, чтобы потом их можно было скормить функциям из TopoCoordTransformer
        n = len(self.target_names)
        i = 0
        while (i < n):
            m = len(self.target_trajectories[i])
            current_trajectory = []
            long_slice = []
            lat_slice = []
            alt_slice = []
            j = 0
            while (j < m - 1):
                delta_long = self.target_trajectories[i][j + 1][0] - self.target_trajectories[i][j][0]
                delta_lat = self.target_trajectories[i][j + 1][1] - self.target_trajectories[i][j][1]
                delta_alt = self.target_trajectories[i][j + 1][2] - self.target_trajectories[i][j][2]
                delta = max(abs(delta_long), abs(delta_lat))
                L = math.floor(delta / dx)
                d_long = delta_long / L
                d_lat = delta_lat / L
                d_alt = delta_alt / L
                k = 0
                while (k < L):
                    point = [self.target_trajectories[i][j][0] + k * d_long, self.target_trajectories[i][j][1] + k * d_lat, self.target_trajectories[i][j][2] + k * d_lat]
                    current_trajectory.append(point)
                    long_slice.append(self.target_trajectories[i][j][0] + k * d_long)
                    lat_slice.append(self.target_trajectories[i][j][1] + k * d_lat)
                    alt_slice.append(self.target_trajectories[i][j][2] + k * d_alt)
                    k = k + 1        
                j = j + 1
            self.approx_target_trajectories.append(current_trajectory)
            self.long_slice_list.append(long_slice)
            self.lat_slice_list.append(lat_slice)
            self.alt_slice_list.append(alt_slice)
            i = i + 1           
    def show_trajectories(self, dx):
        self.traject_approx(dx)
        radar_positions = self.xradar_positions + self.lradar_positions
        radar_names = self.xradar_names + self.lradar_names
        n = len(radar_names)
        m = len(self.target_names)
        i = 0
        while (i < n):
            #print(radar_names[i])
            fig = plt.figure()
            ax = fig.add_subplot(111, projection='3d')
            tct = misc.TopoCoordTransformer(radar_positions[i][0], radar_positions[i][1], radar_positions[i][2])
            j = 0
            while (j < m):
                # N = A.lonlatalt_to_xyz_geocent(C.long_slice_list[0], C.lat_slice_list[0], C.alt_slice_list[0])
                # M = A.xyz_geocent_to_xyz_topo(N[0], N[1], N[2])
                top = tct.lonlatalt_to_xyz_topo(self.long_slice_list[j], self.lat_slice_list[j], self.alt_slice_list[j])
                ax.scatter(top[0], top[1], top[2], c='b', marker='o')
                ax.scatter(radar_positions[i][0], radar_positions[i][1],radar_positions[i][2],  c='r', marker='s')
                ax.set_xlabel('East')
                ax.set_ylabel('North')
                ax.set_zlabel('Z')
                j = j + 1
            #ax.set_aspect(1.0)
            plt.show()
            i = i + 1


class TargetMotion:
    def __init__(self, target_velocity, ctrl_points):
        self.v = target_velocity
        self.control_points = ctrl_points
        self.n = len(self.control_points)
        self.long_slice = []
        self.lat_slice = []
        self.alt_slice = []
        self.xyz_geo = []
        self.l_slice = []
        self.x_l = None
        self.y_l = None
        self.z_l = None

    def subdividing(self, dx): # добавляем точек, чтоб самолет не чиркал землю, как и в RadarSceneData
        for i in range(self.n - 1):
            delta_long = self.control_points[i + 1][0] - self.control_points[i][0]
            delta_lat = self.control_points[i + 1][1] - self.control_points[i][1]
            delta_alt = self.control_points[i + 1][2] - self.control_points[i][2]
            delta = (abs(delta_long)**2 + abs(delta_lat)**2)**0.5
            k = math.floor(delta / dx)
            d_long = delta_long / k
            d_lat = delta_lat / k
            d_alt = delta_alt / k
            for j in range(k):
                self.long_slice.append(self.control_points[i][0] + j * d_long)
                self.lat_slice.append(self.control_points[i][1] + j * d_lat)
                self.alt_slice.append(self.control_points[i][2] + j * d_alt)

    def parametrization(self):  # каждой точке траектории сопоставляем значение l, пройденный путь,
        # чтобы потом использовать одномерную интерполяцию для каждой отдельной координаты
        tct = misc.TopoCoordTransformer(0, 0, 0)
        self.xyz_geo = tct.lonlatalt_to_xyz_geocent(self.long_slice, self.lat_slice, self.alt_slice)
        # переводим в xyz_geocent, чтобы пифагорить
        n = len(self.xyz_geo[0])
        l = 0
        for i in range(n):
            self.l_slice.append(l)
            if i < n - 1:
                delta_l = ((self.xyz_geo[0][i + 1] - self.xyz_geo[0][i]) ** 2 +
                           (self.xyz_geo[1][i + 1] - self.xyz_geo[1][i]) ** 2 +
                           (self.xyz_geo[2][i + 1] - self.xyz_geo[2][i]) ** 2) ** 0.5
                l = l + delta_l
        self.x_l = interpolate.interp1d(self.l_slice, self.xyz_geo[0])
        self.y_l = interpolate.interp1d(self.l_slice, self.xyz_geo[1])
        self.z_l = interpolate.interp1d(self.l_slice, self.xyz_geo[2])

    def showing_earth(self):
        dphi, dtheta = np.pi / 1000.0, np.pi / 1000.0
        [phi, theta] = np.mgrid[0:np.pi:dphi, 0:2 * np.pi:dtheta]
        a = misc.EARTH_SEMIMAJOR
        b = misc.EARTH_SEMIMINOR
        x = a * np.cos(phi) * np.cos(theta)
        y = a * np.cos(theta) * np.sin(phi)
        z = b * np.sin(theta)
        s = mesh(x, y, z)
        return s

    def showing_traject(self):
        l_new = np.arange(0, (self.l_slice[-1]//1000)*1000, 1000)  # округлим l max до км
        x_new = self.x_l(l_new)
        y_new = self.y_l(l_new)
        z_new = self.z_l(l_new)

        return points3d(x_new, y_new, z_new, colormap="copper", scale_factor=10000)

    def __call__(self, t):
        l = self.v * t
        if l < self.l_slice[-1]:
            return (float(self.x_l(l)), float(self.y_l(l)), float(self.z_l(l))), \
                   (self.x_l(l+self.v) - self.x_l(l),
                    self.y_l(l+self.v) - self.y_l(l),
                    self.z_l(l+self.v) - self.z_l(l))
            #  возвращаем тупли xyz_geocent(t), v_geocent(t)


if __name__ == "__main__":
    rsd = RadarSceneData("greece2.kml") #наш рабочий пример
    #rsd.show_trajectories(0.05)
    tm = TargetMotion(250, rsd.target_trajectories[0])
    tm.subdividing(0.1)
    tm.parametrization()
    print(tm(200))
    tm.showing_earth()
    tm.showing_traject()
    show()
    #tm.showing(200)