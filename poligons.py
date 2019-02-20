from shapely.geometry import LineString, Polygon, Point
import numpy as np
from mayavi.mlab import *
import geopoints
import misc


class RainPolygon:

    def __init__(self, polygon, max_hight, area_id = 1, area_name = 'default_name'):
        self.area_id = area_id
        self.area_name = area_name
        self.max_hight = max_hight
        self.polygon = polygon


class RainAreas:

    def __init__(self, lon0, lat0, h0):
        #положение локатора, h0 в киллометрах!
        self.lon0 = lon0
        self.lat0 = lat0
        self.h0 = h0

        #парамтры сетки для grid_procedure
        self.r_min =0.1
        self.r_max = 50
        self.n_r = 499

        self.az_min = 0
        self.az_max = 90
        self.n_az = 90

        self.e_min = 0
        self.e_max = 10
        self.n_e = 10

        self.polygon_list = []
        self.tct = misc.TopoCoordTransformer(0, 0, 0)  #для визуализации


    def add_polygon_directly(self,polygon, h, name='default_name'):
        area_id = len(self.polygon_list) + 1
        area_name = name
        self.polygon_list.append(RainPolygon(polygon, h, area_id, area_name))


    def add_polygon(self, rain_polygon):
        self.polygon_list.append(rain_polygon)


    def add_squere_polygon(self, lon1, lat1, a, h, name):
    #  добавляет квадратный полигон
        area_id = len(self.polygon_list) + 1
        area_name = name
        polygon = [(lon1 + a, lat1 + a), (lon1 + a, lat1 - a), (lon1 - a, lat1 - a), (lon1 - a, lat1 + a), (lon1 + a, lat1 + a)]
        self.polygon_list.append(RainPolygon(polygon, h, area_id, area_name))


    def ray_polyline_projection(self, max_dist, eps, az, refr=True):
    #  возвращает полилинию проекции луча на поверхность, и ray для визуализации луча
        polyline = []
        ray = []
        eps = np.pi * eps / 180
        n = (max_dist // 10) + 1
        for i in range(n + 1):
            dist = i * max_dist / n
            l = geopoints.l(dist, eps, refr)
            (lon, lat) = geopoints.lon_lat_new_point(self.lon0, self.lat0, az, l)
            polyline.append((lon, lat))
            h = (geopoints.h1(dist, eps, refr) + self.h0) * 1000
            ray.append((lon, lat, h))
        return polyline, ray


    def intersection_list(self, polyline):
    #  возвращает пересечание полилинии проекции и полигонов, это тоже полилинии
        intersections = []
        #empty = 0
        for polygon in self.polygon_list:
            shapely_poly = Polygon(polygon.polygon)
            shapely_line = LineString(polyline)
            try:
                intersection_line = list(shapely_poly.intersection(shapely_line).coords)
                if len(intersection_line) > 1:
                    intersections.append((polygon.area_id, polygon.area_name, intersection_line))
                else: intersections.append(None)
            except NotImplementedError:
                #print("Исключение(вызывается, если полигон не пересекся с проекцией луча)")
                intersections.append(None)
        #print('empty', empty)
        return intersections

    def hight_filtration(self, intersections, eps, az, refr=True):
    #  для каждого пересечения возвращает 2 3d точки, "настоящие" точки прересечения луча с полигонами.
    #  для этого выясняется, в какой точке луч достигает max_hight соответствующего полигона, и если она лежит внутри
    #  то она и будет новой точкой выхода луча из полигона
        true_ints = []
        eps = np.pi * eps / 180
        for intersection in intersections:
            if intersection == None:
                true_ints.append(None)
            else:
                id, name, line = intersection[0], intersection[1], intersection[2]
                h = self.polygon_list[id - 1].max_hight
                h1 = h - self.h0
                if h1 <= 0:
                    true_ints.append(None)
                else:
                    dist = geopoints.d_from_h1(h1, eps, refr)
                    l = geopoints.l(dist, eps, refr)
                    point1 = line[0]
                    point2 = line[-1]
                    flag = False
                    if geopoints.l_from_points((self.lon0, self.lat0), point1) < l:
                        if geopoints.l_from_points((self.lon0, self.lat0), point2) >= l:
                            point2 = geopoints.lon_lat_new_point(self.lon0, self.lat0, az, l)
                            flag = True
                        l1 = geopoints.l_from_points((self.lon0, self.lat0), point1)
                        l2 = geopoints.l_from_points((self.lon0, self.lat0), point2)
                        hp1 = geopoints.h1_from_l(l1, eps, refr) + self.h0
                        if flag == True:
                            hp2 = h
                        else:
                            hp2 = geopoints.h1_from_l(l2, eps, refr) + self.h0
                        d1 = geopoints.d_from_h1(hp1 - self.h0, eps, refr)
                        d2 = geopoints.d_from_h1(hp2 - self.h0, eps, refr)
                        lon1, lat1 = point1
                        lon2, lat2 = point2
                        point1_3d = (lon1, lat1, hp1)
                        point2_3d = (lon2, lat2, hp2)
                        true_ints.append((id, name, (point1_3d, point2_3d),(d1, d2)))
                    else: true_ints.append(None)
        return true_ints


    def complete_procedure(self, max_dist, eps, az, refr=True):
        polyline, ray = self.ray_polyline_projection(max_dist, eps, az, refr)
        intersections = self.intersection_list(polyline)
        true_ints = self.hight_filtration(intersections, eps, az, refr)
        return true_ints


    def grid_procedure(self):
    # для точек сетки возвращает массив из id полигона, в который они попадают, или 0, если никуда не попали
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
                    for polygon in self.polygon_list:
                        if Polygon(polygon.polygon).contains(project_point) == True:
                            h = self.h0 + geopoints.h1(r, e)
                            if h <= polygon.max_hight:
                                arr[i][j][k] = polygon.area_id
        return arr


    def ints_angle_grid(self):
        az_range = np.linspace(self.az_min, self.az_max, self.n_az)
        e_range = np.linspace(self.e_min, self.e_max, self.n_e)
        ints_angle_grid = []
        for i in range(len(az_range)):
            e_string = []
            for j in range(len(e_range)):
                az = az_range[i]
                e = e_range[j] * np.pi / 180
                ints = self.complete_procedure(self.r_max, e, az)
                if ints == []:
                    e_string.append(None)
                else:
                    e_string.append(ints)
            ints_angle_grid.append(e_string)
        return ints_angle_grid


    def new_grid_procedure(self, ints_angle_grid):
        az_range = np.linspace(self.az_min, self.az_max, self.n_az)
        r_range = np.linspace(self.r_min, self.r_max, self.n_r)
        e_range = np.linspace(self.e_min, self.e_max, self.n_e)
        arr = np.zeros(shape=(self.n_az, self.n_e, self.n_r), dtype=int)
        for i in range(len(az_range)):
            for j in range(len(e_range)):
                for intersection in ints_angle_grid[i][j]:
                    if intersection != None:
                        id, name, points3d, (r1, r2) = intersection
                        for k in range(len(r_range)):
                            r = r_range[k]
                            if r >= r1 and r <= r2:
                                arr[i][j][k] = id
        return arr


    def show_earth_serface_part(self, min_lon, max_lon, min_lat, max_lat):
    # показывает прямоугольный кусочек поверхности Земли
        dphi, dtheta = np.pi / 1000.0, np.pi / 1000.0
        k = np.pi / 180
        if min_lat > max_lat:
            max_lat =+ 360
        min_th, max_th, min_ph, max_ph = k * (min_lon + 360), k * (max_lon + 360), k * (min_lat + 360), k * (max_lat + 360)
        [phi, theta] = np.mgrid[min_ph:max_ph:dphi, min_th:max_th:dtheta]
        a = misc.EARTH_SEMIMAJOR
        b = misc.EARTH_SEMIMINOR
        x = a * np.cos(phi) * np.cos(theta)
        y = a * np.cos(theta) * np.sin(phi)
        z = b * np.sin(theta)
        s = mesh(x, y, z)
        return s


    def show_traj_proj(self, polyline):
    # показывает проекцию луча
        xs = []
        ys = []
        zs = []
        for point in polyline:
            lon, lat = point
            x, y, z = self.tct.lonlatalt_to_xyz_geocent(lon, lat, 0)
            xs.append(x)
            ys.append(y)
            zs.append(z)
        return plot3d(xs, ys, zs, color=(0, 0, 0), tube_radius=500)


    def show_ray(self, ray):
    # показыввает луч
        xs = []
        ys = []
        zs = []
        for point in ray:
            lon, lat, h = point
            x, y, z = self.tct.lonlatalt_to_xyz_geocent(lon, lat, h)
            xs.append(x)
            ys.append(y)
            zs.append(z)
        return plot3d(xs, ys, zs, color=(1, 0, 0), tube_radius=500)


    def show_polygon(self, id):
        xs = []
        ys = []
        zs = []
        poly = self.polygon_list[id]
        h = poly.max_hight * 1000
        for point in poly.polygon:
            lon, lat = point
            x, y, z = self.tct.lonlatalt_to_xyz_geocent(lon, lat, h)
            xs.append(x)
            ys.append(y)
            zs.append(z)
        return plot3d(xs, ys, zs, color=(0, 0, 1), tube_radius=500)


    def new_show_polygon(self, id):
        d_l = 0.1
        xs = []
        ys = []
        zs = []
        poly = self.polygon_list[id]
        h = poly.max_hight * 1000
        for i in range(len(poly.polygon) - 1):
            (lon1, lat1) = poly.polygon[i]
            (lon2, lat2) = poly.polygon[i + 1]
            l = ((lon2 - lon1)**2 + (lat2 - lat1)**2)**0.5
            n = int(l // d_l) + 1
            d_lon = (lon2 - lon1) / n
            d_lat = (lat2 - lat1) / n
            for j in range(n + 1):
                lon = lon1 + j * d_lon
                lat = lat1 + j * d_lat
                x, y, z = self.tct.lonlatalt_to_xyz_geocent(lon, lat, h)
                xs.append(x)
                ys.append(y)
                zs.append(z)
        return plot3d(xs, ys, zs, color=(0, 0, 1), tube_radius=500)


    def show_all_polygons(self):
        for id in range(len(self.polygon_list)):
            self.new_show_polygon(id)


    def show_intersect_points(self, true_ints):
        xs = []
        ys = []
        zs = []
        for intersection in true_ints:
            if intersection != None:
                id, name, (point1, point2), (d1, d2) = intersection
                lon1, lat1, h1 = point1
                lon2, lat2, h2 = point2
                x, y, z = self.tct.lonlatalt_to_xyz_geocent(lon1, lat1, 1000 * h1)
                xs.append(x)
                ys.append(y)
                zs.append(z)
                x, y, z = self.tct.lonlatalt_to_xyz_geocent(lon2, lat2, 1000 * h2)
                xs.append(x)
                ys.append(y)
                zs.append(z)
        return points3d(xs, ys, zs,colormap="copper", scale_factor=1000)


    def show_grid(self, arr):
        in_x = []
        in_y = []
        in_z = []
        out_x = []
        out_y = []
        out_z = []
        az_range = np.linspace(self.az_min, self.az_max, self.n_az)
        r_range = np.linspace(self.r_min, self.r_max, self.n_r)
        e_range = np.linspace(self.e_min, self.e_max, self.n_e)
        for i in range(len(az_range)):
            for j in range(len(e_range)):
                for k in range(len(r_range)):
                    az = az_range[i]
                    e = e_range[j] * np.pi / 180
                    r = r_range[k]
                    l = geopoints.l(r, e)
                    (lon, lat) = geopoints.lon_lat_new_point(self.lon0, self.lat0, az, l)
                    h = self.h0 + geopoints.h1(r, e)
                    x, y, z = self.tct.lonlatalt_to_xyz_geocent(lon, lat, 1000 * h)
                    if arr[i][j][k] == 0:
                        out_x.append(x)
                        out_y.append(y)
                        out_z.append(z)
                    else:
                        in_x.append(x)
                        in_y.append(y)
                        in_z.append(z)
        return points3d(in_x, in_y, in_z,color=(1,1,1), scale_factor=1000), points3d(out_x, out_y, out_z,color=(0,0,0), scale_factor=1000)

if __name__ == '__main__':

    areas = RainAreas(0, 0, 5)
    areas.add_squere_polygon(0.2, 0.2, 0.1, 5, '1')
    areas.add_squere_polygon(0, 0, 0.2, 10, '2')
    #ints_angle_grid = areas.ints_angle_grid()
    #arr = areas.new_grid_procedure(ints_angle_grid)
    polyline, ray = areas.ray_polyline_projection(1000, 0, 45, refr=False)
    true_ints = areas.complete_procedure(1000, 0, 45, refr=False)
    #true_ints = areas.ints_angle_grid()
    print(true_ints)
    areas.show_earth_serface_part(-10,10,-10,10)
    #areas.new_show_polygon(0)
    areas.show_all_polygons()
    #areas.show_grid(arr)
    areas.show_traj_proj(polyline)
    areas.show_ray(ray)
    areas.show_intersect_points(true_ints)
    show()
    #print(arr[0][0])
