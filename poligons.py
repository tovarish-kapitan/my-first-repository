from shapely.geometry import LineString, Polygon, Point
import numpy as np
import geopoints

#polygon = [(0.0, 0.0), (3.0, 0.0), (3.0, 2.0), (2.0, 2.0), (2.0, 1.0), (1.0, 1.0), (1.0, 2.0), (0.0, 2.0), (0.0, 0.0)]
#shapely_poly = Polygon(polygon)

#line = [(-1.0, 0.0), (2.0, 0.0)]
#shapely_line = LineString(line)

#intersection_line = list(shapely_poly.intersection(shapely_line).coords)
#print(intersection_line)

class RainPoligon:

    def __init__(self, area_id, area_name, max_hight, poligon):
        self.area_id = area_id
        self.area_name = area_name
        self.max_hight = max_hight
        self.poligon = poligon


class RainAreas:

    def __init__(self, lon0, lat0, h0):

        self.lon0 = lon0
        self.lat0 = lat0
        self.h0 = h0

        self.r_min = 0
        self.r_max = 100
        self.n_r = 10

        self.az_min = 0
        self.az_max = 90
        self.n_az = 10

        self.e_min = 0
        self.e_max = 10
        self.n_e = 10

        self.poligon_list = []

    def add_squere_poligon(self, lon1, lat1, a, h, id, name):
        area_id = id
        area_name = name
        poligon = [(lon1 + a, lat1 + a), (lon1 + a, lat1 - a), (lon1 - a, lat1 - a), (lon1 - a, lat1 + a)]
        self.poligon_list.append(RainPoligon(area_id, area_name, h, poligon))


    def chess_poligons_init(self, n, l, h):
        k = 1
        for i in range(-n, n, 1):
            for j in range(-n, n, 1):
                #if (i + j) // 2 == 0:
                    lon1 = self.lon0 + i * l
                    lat1 = self.lat0 + j * l
                    poligon = [(lon1, lat1), (lon1 + l, lat1), (lon1 + l, lat1 + l), (lon1, lat1 + 1)]
                    area_id = k
                    k = k + 1
                    area_name = '%s_%s' % (i, j)
                    self.poligon_list.append(RainPoligon(area_id, area_name, h, poligon))
        #print(k, 'poligons')


    def ray_polyline_projection(self, max_dist, n, eps, az):
        polyline = []
        eps = np.pi * eps / 180
        for i in range(n + 1):
            dist = i * max_dist / n
            l = geopoints.l(dist, eps)
            projection_point = geopoints.lon_lat_new_point(self.lon0, self.lat0, az, l)
            polyline.append(projection_point)
        return polyline


    def intersection_list(self, polyline):
        intersections = []
        #empty = 0
        for poligon in self.poligon_list:
            shapely_poly = Polygon(poligon.poligon)
            shapely_line = LineString(polyline)
            try:
                intersection_line = list(shapely_poly.intersection(shapely_line).coords)
                if len(intersection_line) > 1:
                    intersections.append((poligon.area_id, poligon.area_name, intersection_line))
            except NotImplementedError:
                #print("Исключение(вызывается, если полигон не пересекся с проекцией луча)")
                empty = empty + 1
        #print('empty', empty)
        return intersections

    def hight_filtration(self, intersections, eps, az):
        true_ints = []
        eps = np.pi * eps / 180
        for intersection in intersections:
            id, name, line = intersection[0], intersection[1], intersection[2]
            h = self.poligon_list[id].max_hight
            h1 = h - self.h0
            dist = geopoints.d_from_h1(h1, eps)
            l = geopoints.l(dist, eps)
            #print(id, h, l)
            point1 = line[0]
            point2 = line[-1]
            #print(geopoints.l_from_points((self.lon0, self.lat0), point1))
            if geopoints.l_from_points((self.lon0, self.lat0), point1) < l:
                if geopoints.l_from_points((self.lon0, self.lat0), point2) >= l:
                    #print(geopoints.lon_lat_new_point(self.lon0, self.lat0, az, l))
                    point2 = geopoints.lon_lat_new_point(self.lon0, self.lat0, az, l)
                l1 = geopoints.l_from_points((self.lon0, self.lat0), point1)
                l2 = geopoints.l_from_points((self.lon0, self.lat0), point2)
                hp1 = geopoints.h1_from_l(l1, eps) + self.h0
                hp2 = geopoints.h1_from_l(l2, eps) + self.h0
                lon1, lat1 = point1
                lon2, lat2 = point2
                point1_3d = (lon1, lat1, hp1)
                point2_3d = (lon2, lat2, hp2)
                true_ints.append((id, name, (point1_3d, point2_3d)))
        return true_ints


    def complite_procedure(self, max_dist, n, eps, az):
        polyline = self.ray_polyline_projection(max_dist, n, eps, az)
        intersections = self.intersection_list(polyline)
        true_ints = self.hight_filtration(intersections, eps, az)
        return true_ints


    def grid_procedure(self):
        az_range = np.linspace(self.az_min, self.az_max, self.n_az)
        r_range = np.linspace(self.r_min, self.r_max, self.n_r)
        e_range = np.linspace(self.e_min, self.e_max, self.n_e)
        arr = np.zeros(shape=(self.n_az, self.n_e, self.n_r), dtype=int)
        for i in range(len(az_range)):
            for j in range(len(e_range)):
                for k in range(len(r_range)):
                    az = az_range[i]
                    e = e_range[j] * np.pi / 180
                    r = r_range[k]
                    l = geopoints.l(r, e)
                    (lon, lat) = geopoints.lon_lat_new_point(self.lon0, self.lat0, az, l)
                    project_point = Point(lon, lat)
                    for poligon in self.poligon_list:
                        if Polygon(poligon.poligon).contains(project_point) == True:
                            h = self.h0 + geopoints.h1(r, e)
                            if h <= poligon.max_hight:
                                arr[i][j][k] = poligon.area_id
        return arr



if __name__ == '__main__':

    areas = RainAreas(0, 0, 0)
    #areas.poligon_list.append(RainPoligon(1, 1, ((0.0, 0.0), (2.0, 0.0), (2.0, 2.0), (0.0, 2.0))))
    #areas.chess_poligons_init(3, 0.1, 20)
    areas.add_squere_poligon(0.2, 0.2, 0.15, 1, 1, '1')
    areas.add_squere_poligon(0.6, 0.6, 0.2, 10, 2, '2')
    arr = areas.grid_procedure()
    #true_ints = areas.complite_procidure(1000, 10, 0, 45)
    #line = areas.ray_polyline_projection(1000, 1, 0, 45)
    #ints = areas.intersection_list(line)
    #true_ints = areas.hight_filtration(ints, 0, 45)
    print(arr)

    #print(true_ints)
    #print(a)