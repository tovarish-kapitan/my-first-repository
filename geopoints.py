import geopy
import numpy as np
from geopy.distance import VincentyDistance, vincenty

R_EFF = 4 * 6400 / 3


def lon_lat_new_point(lon0, lat0, az, dist):
    origin = geopy.Point(lon0, lat0)
    destination = VincentyDistance(kilometers=dist).destination(origin, az)
    lat, lon = destination.latitude, destination.longitude
    return (lon, lat)


def lon_lat_line_set(lon0, lat0, az, max_dist=100, steps=10):
    step = max_dist / steps
    set = []
    for i in range(steps + 1):
        point = lon_lat_new_point(lon0, lat0, az, i*step)
        set.append(point)
    return set


def h1(d, eps):
    #eps = np.pi * eps / 180
    return d * np.sin(eps) + 0.5 * d * d * np.cos(eps) ** 2 / R_EFF


def l(d, eps):
    #eps = np.pi * eps / 180
    l = ((d ** 2 - h1(d, eps) ** 2) / (1 + h1(d, eps) / R_EFF)) ** 0.5
    return l


def d_from_h1(h, eps):
    #eps = np.pi * eps / 180
    dist = - np.sin(eps) * R_EFF / np.cos(eps) ** 2 + ((np.sin(eps) * R_EFF / np.cos(eps) ** 2)**2
                                                       + 2 * R_EFF * h / np.cos(eps) ** 2) ** 0.5
    return dist


def l_from_points(point1, point2):
    return(vincenty(point1, point2).kilometers)


def d_from_l(l, eps):
    if l == 0:
        return 0
    else:
    #eps = np.pi * eps / 180
        b = 2 * np.sin(eps) / R_EFF
        a = (np.cos(eps)) ** 2 * (3 / (4 * R_EFF ** 2) - 1 / (l ** 2))
        d = 0.5 * ((b ** 2 - 4 * a) ** 0.5 - b) / a
        return d


def h1_from_l(l, eps):
    return h1(d_from_l(l, eps), eps)
