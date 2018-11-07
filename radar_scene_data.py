import math
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from bs4 import BeautifulSoup
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
    def traject_approx(self, dx):  #разбивает отрезки между точками траектории с шагом не более чем dx
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
                   
if __name__ == "__main__":
    import sys
    C = RadarSceneData("greece2.kml") #наш рабочий пример
    C.traject_approx(0.1)
    radar_positions = C.xradar_positions + C.lradar_positions
    radar_names = C.xradar_names + C.lradar_names
    #print(radar_names)
    n = len(radar_positions)
    #print(n)
    m = len(C.target_names)
    i = 0
    while (i < n):
        print(radar_names[i])
        fig = plt.figure()
        ax = fig.add_subplot(111)
        A = misc.TopoCoordTransformer(radar_positions[i][0], radar_positions[i][1], radar_positions[i][2])
        j = 0
        while (j < m):
            #N = A.lonlatalt_to_xyz_geocent(C.long_slice_list[0], C.lat_slice_list[0], C.alt_slice_list[0])
            #M = A.xyz_geocent_to_xyz_topo(N[0], N[1], N[2])
            K = A.lonlatalt_to_xyz_topo(C.long_slice_list[j], C.lat_slice_list[j], C.alt_slice_list[j])
            ax.scatter(C.long_slice_list[j], C.lat_slice_list[j], c='b', marker='o')
            ax.scatter(radar_positions[i][0], radar_positions[i][1], c='r', marker='s')
            ax.set_xlabel('East')
            ax.set_ylabel('North')
            # ax.set_zlabel('Z')
            j = j + 1
        ax.set_aspect(1.0)
        plt.show()    
        i = i + 1
    
