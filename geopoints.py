import geopy
import numpy as np
from geopy.distance import VincentyDistance, vincenty
import misc

ER = misc.EARTH_RADIUS * 0.001


def lon_lat_new_point(lon0, lat0, az, dist):
#  возвращает новую точку, через азимут и расстояние от данной точки
    origin = geopy.Point(lon0, lat0)
    destination = VincentyDistance(kilometers=dist).destination(origin, az)
    lat, lon = destination.latitude, destination.longitude
    return (lon, lat)


def h1(d, eps, refr=True):
#  высота подъема луча через его длину и угол возвышения
    if refr==True:
        r_eff = ER * 4 / 3
    else:
        r_eff = ER
    return d * np.sin(eps) + 0.5 * d * d * np.cos(eps) ** 2 / r_eff


def l(d, eps, refr=True):
#  длина проекции луча через его длину и угол возвышения
    if refr == True:
        r_eff = ER * 4 / 3
    else:
        r_eff = ER
    l = ((d ** 2 - h1(d, eps, refr) ** 2) / (1 + h1(d, eps, refr) / r_eff)) ** 0.5
    return l


def d_from_h1(h, eps, refr=True):
#   длина луча через высоту его поднятия и угол возвышения
    if refr == True:
        r_eff = ER * 4 / 3
    else:
        r_eff = ER
    dist = - np.sin(eps) * r_eff / np.cos(eps) ** 2 + ((np.sin(eps) * r_eff / np.cos(eps) ** 2)**2
                                                       + 2 * r_eff * h / np.cos(eps) ** 2) ** 0.5
    return dist


def l_from_points(point1, point2):
# расстояние по поверхности между двумя точками на поверхности
    return(vincenty(point1, point2).kilometers)


def d_from_l(l, eps, refr=True):
#  длина проекции луча через его длину и угол возвышения
    if refr == True:
        r_eff = ER * 4 / 3
    else:
        r_eff = ER
    if l == 0:
        return 0
    else:
        b = 2 * np.sin(eps) / r_eff
        a = (np.cos(eps)) ** 2 * (1 / (l ** 2) - 3 / (4 * r_eff ** 2))
        d = 0.5 * ((b ** 2 + 4 * a) ** 0.5 + b) / a
        return d


def h1_from_l(l, eps, refr=True):
# высота подъема луча через длину его проекции и угол возвышения
    return h1(d_from_l(l, eps, refr), eps, refr)

#print(h1(1000, 0, refr=True))
#print(h1(1000, 0, refr=False))