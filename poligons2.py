import poligons


#this checks the sign of a number
def sign(x):
    if x >= 0: return 1
    else: return 0

#this defines triples of subsequent vertexes on any polygon
def triads(p):
    return zip(p, p[1:]+[p[0]], p[2:]+[p[0]]+[p[1]])

#this uss Bastian's three-vertex function to check convexity
def check_convexity(p):
    i = 0
    for ((x0, y0), (x1, y1), (x2,y2)) in triads(p):
        if i==0: fsign = sign(x2*(y1-y0)-y2*(x1-x0)+(x1-x0)*y0-(y1-y0)*x0)
        else:
            newsign = sign(x2*(y1-y0)-y2*(x1-x0)+(x1-x0)*y0-(y1-y0)*x0)
            if newsign != fsign: return False
        i +=1
    return True


def dict_rain_from_normal_rain(list_of_points, height):
    anchors = []
    for point in list_of_points:
        (lon, lat) = point
        dict_point = {'lat': lat, 'lon': lon}
        anchors.append(dict_point)
    rain = {'anchors': anchors, 'height': height}
    return rain


def normal_rain_from_dict_rain(rain):
    anchors = rain['anchors']
    list_of_points = []
    for anchor in anchors:
        lon = anchor['lon']
        lat = anchor['lat']
        list_of_points.append((lon, lat))
    h = rain['height'] * 0.001  #  внутри RainAreas h в километрах пока-что
    return list_of_points, h


def intersection_lenghts(rains, llh, ray, refr=True):
    intersection_lenghts = []
    lon0 = llh['lon']
    lat0 = llh['lat']
    h0 = llh['height']
    rain_areas = poligons.RainAreas(lon0, lat0, h0 * 0.001)  #  внутри RainAreas h в километрах пока-что
    for rain in rains:
        list_of_points, h = normal_rain_from_dict_rain(rain)
        if check_convexity(list_of_points) == True:
            rain_areas.add_polygon_directly(list_of_points, h)
        else:
            print(rain, 'polygon is inconvex')
    az = ray['azimuth']
    e = ray['elevation']
    r = ray['distance']
    true_ints = rain_areas.complete_procedure(r, e, az, refr)
    for intersection in true_ints:
        if intersection == None:
            intersection_lenghts.append(None)
        else:
            (id, name, (point1_3d, point2_3d), (d1, d2)) = intersection
            d = (d2 - d1) * 1000  #  длина пересечения в метрах
            intersection_lenghts.append(d)
    return intersection_lenghts


if __name__ == '__main__':

    az = 45
    e = 15
    d = 1000
    lon0 = 0
    lat0 = 0
    h0 = 0

    ray = {'azimuth': az, 'elevation': e, 'distance': d}
    llh = {'lon': lon0, 'lat': lat0, 'height': h0}

    list_of_points1 = [(0.2, 0.2), (0.1 , 0.0), (0.2, -0.2), (-0.2, -0.2), (-0.2, 0.2), (0.2, 0.2)]
    h1 = 5000

    list_of_points2 = [(0.1, 0.1), (0.1, 0.3), (0.3, 0.3), (0.3, 0.1), (0.1, 0.1)]
    h2 = 10000

    rain1 = dict_rain_from_normal_rain(list_of_points1, h1)
    print(rain1)

    rain2 = dict_rain_from_normal_rain(list_of_points2, h2)
    print(rain2)

    ints = intersection_lenghts([rain1, rain2], llh, ray, refr=True)
    print(ints)