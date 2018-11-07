# -*- coding: UTF-8 -*-

import numpy as np
import scipy as sp
import scipy.linalg
import pyproj

import matplotlib.pyplot as plt

EARTH_SEMIMINOR = 6356752.314245  # earth sizes (WGS84 sizes )...
EARTH_SEMIMAJOR = 6378137.0
EARTH_RADIUS = 6370997.0


class XYZCoordTransformer(object):
    """
    We want to from old basis to new one. We create new ``x'``, ``y'``, and ``z'`` vectors (in old basis) and
        provide the new basis' point of origin (in old basis coordinates).
    """
    def __init__(self, x_axis_vec, y_axis_vec, z_axis_vec, origin_vec):
        """
        Args:
            x_axis_vec (array-like): new X axis given in old coordinate system as (x, y, z) vector
            y_axis_vec (array-like):
            z_new_vec (array-like):
            origin_vec (array-like):
        """

        self._x_axis_vec = np.asarray(x_axis_vec, dtype=np.float64)
        self._y_axis_vec = np.asarray(y_axis_vec, dtype=np.float64)
        self._z_axis_vec = np.asarray(z_axis_vec, dtype=np.float64)
        self._origin_vec = np.asarray(origin_vec, dtype=np.float64)

        assert self._x_axis_vec.shape == (3,)
        assert self._y_axis_vec.shape == (3,)
        assert self._z_axis_vec.shape == (3,)
        assert self._origin_vec.shape == (3,)

        self._affine_matrix_inv = np.asarray([self._x_axis_vec, self._y_axis_vec, self._z_axis_vec]).swapaxes(0, 1)
        self._affine_matrix = sp.linalg.inv(self._affine_matrix_inv)

    def old_to_new_coords(self, old_coords):
        """
        Args:
            old_coords(array-like): a ``3-by-N`` array, where ``N`` is the number of points to convert

        Returns:
            out_data(:class:`numpy.ndarray(dtype=np.float64)`): converted data array with shape ``3-by-N``
        """

        old_coords = np.asarray(old_coords, dtype=np.float64)
        assert len(old_coords.shape) == 2
        assert old_coords.shape[0] == 3

        return np.dot(self._affine_matrix, old_coords - self._origin_vec[:, None])

    def new_to_old_coords(self, new_coords):
        """
        Args:
            vec_data(array-like): a ``3-by-N`` array, where ``N`` is the number of points to convert
        """
        new_coords = np.asarray(new_coords, dtype=np.float64)
        assert len(new_coords.shape) == 2
        assert new_coords.shape[0] == 3

        return np.dot(self._affine_matrix_inv, new_coords) + self._origin_vec[:, None]


def degminsec2decimal(degs=0, mins=0, secs=0):
    return degs + mins / 60. + secs / 3600.


def decimal2degminsec(decimal=0):
    degs = int(decimal)
    mins = int((decimal - degs) * 60)
    secs = int((decimal - degs - mins / 60.) * 3600)
    return degs, mins, secs


def distances_to_sealevel(lat_center, lon_center, x_mesh_ortho, y_mesh_ortho, eff_earth_ratio=(4. / 3.)):
    """
    Расстояния от плоскости, касательной к земному эллипсоиду, опущенные к  уровню моря
        через точки с координатами `x_mesh_ortho` и `y_mesh_ortho` в ортопроекции
    :param lat_center:
    :param lon_center:
    :param x_mesh_ortho:
    :param y_mesh_ortho:
    :param eff_earth_ratio:
    :return:
    """
    assert isinstance(x_mesh_ortho, np.ndarray)
    assert isinstance(y_mesh_ortho, np.ndarray)

    assert len(x_mesh_ortho.shape) == 2
    assert len(y_mesh_ortho.shape) == 2
    assert y_mesh_ortho.shape == x_mesh_ortho.shape

    eff_earth_semiminor = EARTH_SEMIMAJOR * eff_earth_ratio
    eff_earth_semimajor = EARTH_SEMIMAJOR * eff_earth_ratio
    eff_earth_radius = EARTH_RADIUS * eff_earth_ratio

    ortho_refraction = pyproj.Proj(proj="ortho", ellps='WGS84',  lat_0=lat_center, lon_0=lon_center,
                                  units="m", a=eff_earth_semimajor, b=eff_earth_semiminor)

    ecef_refraction = pyproj.Proj(proj='geocent', ellps='WGS84', x_0=0, y_0=0,
                                  units="m", a=eff_earth_semimajor, b=eff_earth_semiminor)

    z_mesh_ortho = np.zeros_like(x_mesh_ortho)

    # Converting from ORTHO to ECEF
    x_mesh_ecef, y_mesh_ecef, z_mesh_ecef = pyproj.transform(ortho_refraction, ecef_refraction,
                                                             x_mesh_ortho, y_mesh_ortho, z_mesh_ortho)
    ecef_data_vec = np.stack((x_mesh_ecef, y_mesh_ecef, z_mesh_ecef), axis=0).reshape(3, x_mesh_ortho.size)

    # Preparing to switch to new affine coordinate system (X to east, Y to north, Z to up)
    dx = 1e-2  # m
    x_center, y_center, z_center = pyproj.transform(ortho_refraction, ecef_refraction, 0, 0, 0)
    x_right, y_right, z_right = pyproj.transform(ortho_refraction, ecef_refraction, dx, 0, 0)
    x_left, y_left, z_left = pyproj.transform(ortho_refraction, ecef_refraction, -dx, 0, 0)
    x_up, y_up, z_up = pyproj.transform(ortho_refraction, ecef_refraction, 0, dx, 0)
    x_down, y_down, z_down = pyproj.transform(ortho_refraction, ecef_refraction, 0, -dx, 0)

    vec_center = np.asarray([x_center, y_center, z_center])

    vec_east = np.asarray([x_right - x_left, y_right - y_left, z_right - z_left])
    vec_north = np.asarray([x_up - x_down, y_up - y_down, z_up - z_down])
    vec_up = np.cross(vec_east, vec_north)

    dir_east = vec_east / np.linalg.norm(vec_east)
    dir_north = vec_north / np.linalg.norm(vec_north)
    dir_up = vec_up / np.linalg.norm(vec_up)

    # And now finally we change our coordinate system!
    coord_transformer = XYZCoordTransformer(dir_east, dir_north, dir_up, vec_center)

    new_vec_data = coord_transformer.old_to_new_coords(ecef_data_vec)

    new_vec_data = new_vec_data.reshape([3] + list(x_mesh_ortho.shape))
    sealevel_distances = new_vec_data[2, :, :]

    return x_mesh_ortho, y_mesh_ortho, sealevel_distances


def xy_to_lonlat(lat_stand, lon_stand, x_coords, y_coords):
    latlon_proj = pyproj.Proj(init='EPSG:4326')
    ortho_proj = pyproj.Proj(proj="ortho", ellps='WGS84', datum="WGS84", lat_0=float(lat_stand),
                             lon_0=float(lon_stand), units="m")

    lons, lats = pyproj.transform(ortho_proj, latlon_proj, x_coords, y_coords)
    return lons, lats

def lonlatz_to_ecef(lon_array, lat_array, z_abovesea_array):
    lonlat_proj = pyproj.Proj(init='EPSG:4326')
    ecef_proj = pyproj.Proj(proj="geocent", ellps='WGS84')

    x_array, y_array, z_array = pyproj.transform(lonlat_proj, ecef_proj, lon_array, lat_array, z_abovesea_array)

    return x_array, y_array, z_array


class TopoCoordTransformer(object):
    """
    TODOTODOTODO
    """

    _lla_proj = pyproj.Proj("+proj=latlong +datum=WGS84")
    _ecef_proj = pyproj.Proj(proj='geocent', ellps='WGS84', datum="WGS84")

    _lla_argunsoft_proj = pyproj.Proj("+proj=latlong +ellps=krass +towgs84=23.92,-141.27,-80.91,0,0,0,0")
    # _lla_argunsoft_proj = pyproj.Proj("+init=EPSG:4284 ")

    # FIXME
    _z_correction_ratio = EARTH_SEMIMAJOR / EARTH_SEMIMINOR

    def __init__(self, lon_stand, lat_stand, z_abovesea_stand=0):
        self._lon_stand = float(lon_stand)
        self._lat_stand = float(lat_stand)
        self._z_abovesea_stand = float(z_abovesea_stand)


        delta_deg = 1e-7  # deg delta for derivation (1 deg is about 100km)
        delta_z = 1e-2  # Z delta in meters

        x_center, y_center, z_center = pyproj.transform(self._lla_proj, self._ecef_proj, self._lon_stand,
                                                        self._lat_stand, self._z_abovesea_stand)
        x_right, y_right, z_right = pyproj.transform(self._lla_proj, self._ecef_proj, self._lon_stand + delta_deg,
                                                     self._lat_stand, self._z_abovesea_stand)
        x_left, y_left, z_left = pyproj.transform(self._lla_proj, self._ecef_proj, self._lon_stand - delta_deg,
                                                  self._lat_stand, self._z_abovesea_stand)


        x_up, y_up, z_up = pyproj.transform(self._lla_proj, self._ecef_proj, self._lon_stand,
                                            self._lat_stand + delta_deg, self._z_abovesea_stand)
        x_down, y_down, z_down = pyproj.transform(self._lla_proj, self._ecef_proj,
                                                  self._lon_stand, self._lat_stand - delta_deg, self._z_abovesea_stand)

        z_center *= self._z_correction_ratio
        z_left *= self._z_correction_ratio
        z_right *= self._z_correction_ratio
        z_up *= self._z_correction_ratio
        z_down *= self._z_correction_ratio

        vec_center = np.asarray([x_center, y_center, z_center])

        vec_east = np.asarray([x_right - x_left, y_right - y_left, z_right - z_left])
        vec_north = np.asarray([x_up - x_down, y_up - y_down, z_up - z_down])
        vec_up = np.cross(vec_east, vec_north)

        dir_east = vec_east / np.linalg.norm(vec_east)
        dir_north = vec_north / np.linalg.norm(vec_north)
        dir_up = vec_up / np.linalg.norm(vec_up)



        # And now finally we change our coordinate system!
        self._xyz_transformer = XYZCoordTransformer(dir_east, dir_north, dir_up, vec_center)


    def lonlatalt_to_xyz_topo(self, lon_array, lat_array, z_abovesea_array, use_argunsoft_proj=False):
        """
        Converts LonLatAlt (WGS-84) coordinates to topocentrical XYZ coordiantes (X is East, Y is North, Z is Up).

        Returns:
            x_array
            y_array,
            z_abovesea_array
        """
        lon_array = np.asarray(lon_array, dtype=np.float64)
        lat_array = np.asarray(lat_array, dtype=np.float64)
        z_abovesea_array = np.asarray(z_abovesea_array, dtype=np.float64)

        geocent_data_vec = self._lonlatalt_yo_xyz_geocent_datavec(
            lon_array, lat_array, z_abovesea_array, use_argunsoft_proj)

        new_vec_data = self._xyz_transformer.old_to_new_coords(geocent_data_vec).reshape((3,) + lon_array.shape)

        # new_vec_data = new_vec_data.reshape((3,) + lon_array.shape)

        return new_vec_data[0], new_vec_data[1], new_vec_data[2]

    @staticmethod
    def _lonlatalt_yo_xyz_geocent_datavec(lon_array, lat_array, z_abovesea_array, use_argunsoft_proj):
        assert lon_array.shape == lat_array.shape == z_abovesea_array.shape

        lla_proj = TopoCoordTransformer._lla_argunsoft_proj if use_argunsoft_proj else TopoCoordTransformer._lla_proj

        x_geocent_array, y_geocent_array, z_geocent_array = pyproj.transform(
            lla_proj, TopoCoordTransformer._ecef_proj, lon_array, lat_array, z_abovesea_array)

        z_geocent_array *= TopoCoordTransformer._z_correction_ratio

        geocent_data_vec = np.stack((x_geocent_array, y_geocent_array, z_geocent_array), axis=0).reshape((3, lon_array.size))

        return geocent_data_vec

    @staticmethod
    def lonlatalt_to_xyz_geocent(lon_array, lat_array, z_abovesea_array, use_argunsoft_proj=False):
        """
        Returns:
            x_array
            y_array,
            z_array
        """
        lon_array = np.asarray(lon_array, dtype=np.float64)
        lat_array = np.asarray(lat_array, dtype=np.float64)
        z_abovesea_array = np.asarray(z_abovesea_array, dtype=np.float64)

        geocent_data_vec = TopoCoordTransformer._lonlatalt_yo_xyz_geocent_datavec(
            lon_array, lat_array, z_abovesea_array, use_argunsoft_proj)

        geocent_data_vec = geocent_data_vec.reshape((3,) + lon_array.shape)
        return geocent_data_vec[0], geocent_data_vec[1], geocent_data_vec[2]


    def xyz_topo_to_lonlatalt(self, x_array, y_array, z_array, use_argunsoft_proj=False):
        """
        Converts topocentrical XYZ coordiantes (X is East, Y is North, Z is Up) to LonLatAlt (WGS-84).

        Returns:
            lon_array,
            lat_array,
            z_array
        """
        x_array = np.asarray(x_array, dtype=np.float64)
        y_array = np.asarray(y_array, dtype=np.float64)
        z_array = np.asarray(z_array, dtype=np.float64)

        assert x_array.shape == y_array.shape == z_array.shape
        xyz_data_vec = np.stack((x_array, y_array, z_array), axis=0).reshape((3, x_array.size))
        geocent_data_vec = self._xyz_transformer.new_to_old_coords(xyz_data_vec)

        lla_data_vec = self._xyz_geocent_to_lonlatalt_datavec(
            geocent_data_vec[0], geocent_data_vec[1], geocent_data_vec[2], use_argunsoft_proj)

        lla_data_vec = lla_data_vec.reshape((3,) + x_array.shape)

        return lla_data_vec[0], lla_data_vec[1], lla_data_vec[2]

    @staticmethod
    def _xyz_geocent_to_lonlatalt_datavec(x_geocent, y_geocent, z_geocent, use_argunsoft_proj=False):
        """
        Args:
            x_geocent
            y_geocent
            z_geocent
        Returns:
            :class:`numpy.ndarray(dtype=np.float64)`
        """
        assert x_geocent.shape == y_geocent.shape == z_geocent.shape

        lla_proj = TopoCoordTransformer._lla_argunsoft_proj if use_argunsoft_proj else TopoCoordTransformer._lla_proj

        lon_array, lat_array, z_abovesea_array = pyproj.transform(
            TopoCoordTransformer._ecef_proj, lla_proj, x_geocent, y_geocent,
            z_geocent / TopoCoordTransformer._z_correction_ratio)

        lla_data_vec = np.stack((lon_array, lat_array, z_abovesea_array), axis=0).reshape((3, x_geocent.size))
        return lla_data_vec

    @staticmethod
    def xyz_geocent_to_lonlatalt(x_geocent, y_geocent, z_geocent, use_argunsoft_proj=False):
        """
        Converts geocentrical XYZ coordinates on WGS84 ellipsoid to LonLatAlt (WGS-84).

        Returns:
             x_array,
             y_array,
             z_array
        """
        x_geocent = np.asarray(x_geocent, dtype=np.float64)
        y_geocent = np.asarray(y_geocent, dtype=np.float64)
        z_geocent = np.asarray(z_geocent, dtype=np.float64)

        lla_data_vec = TopoCoordTransformer._xyz_geocent_to_lonlatalt_datavec(
            x_geocent, y_geocent, z_geocent, use_argunsoft_proj)

        lla_data_vec = lla_data_vec.reshape((3,) + x_geocent.shape)
        return lla_data_vec[0], lla_data_vec[1], lla_data_vec[2]

    def xyz_topo_to_xyz_geocent(self, x_topo, y_topo, z_topo):
        x_topo = np.asarray(x_topo, dtype=np.float64)
        y_topo = np.asarray(y_topo, dtype=np.float64)
        z_topo = np.asarray(z_topo, dtype=np.float64)

        assert x_topo.shape == y_topo.shape == z_topo.shape

        xyz_topo_datavec = np.stack((x_topo, y_topo, z_topo), axis=0).reshape((3, x_topo.size))

        xyz_geocent_datavec = self._xyz_transformer.new_to_old_coords(xyz_topo_datavec)

        xyz_geocent_data = xyz_geocent_datavec.reshape((3,) + x_topo.shape)

        return xyz_geocent_data[0], xyz_geocent_data[1], xyz_geocent_data[2]

    def xyz_geocent_to_xyz_topo(self, x_geocent, y_geocent, z_geocent):
        """
        Converts geocentrical XYZ coordinates on WGS84 ellipsoid to XYZ topocentrical coordinates
            (X is East, Y is North, Z is Up).
        :param x_geocent:
        :param y_geocent:
        :param z_geocent:
        :return:
        """
        x_geocent = np.asarray(x_geocent, dtype=np.float64)
        y_geocent = np.asarray(y_geocent, dtype=np.float64)
        z_geocent = np.asarray(z_geocent, dtype=np.float64)
        assert x_geocent.shape == y_geocent.shape == z_geocent.shape

        xyz_geocent_datavec = np.stack((x_geocent, y_geocent, z_geocent), axis=0).reshape((3, x_geocent.size))
        xyz_topo_datavec = self._xyz_transformer.old_to_new_coords(xyz_geocent_datavec)

        xyz_topo_data = xyz_topo_datavec.reshape((3,) + x_geocent.shape)
        return xyz_topo_data[0], xyz_topo_data[1], xyz_topo_data[2]

    @staticmethod
    def lonlatalt_argunsoft_to_wgs(lon_array, lat_array, z_abovesea_array):
        return pyproj.transform(
            TopoCoordTransformer._lla_argunsoft_proj, TopoCoordTransformer._lla_proj,
            lon_array, lat_array, z_abovesea_array)

    @staticmethod
    def lonlatalt_wgs_to_argunsoft(lon_array, lat_array, z_abovesea_array):
        return pyproj.transform(
            TopoCoordTransformer._lla_proj, TopoCoordTransformer._lla_argunsoft_proj,
            lon_array, lat_array, z_abovesea_array)


if __name__ == "__main__":

    ecef_proj = TopoCoordTransformer._ecef_proj
    lonlat_proj = TopoCoordTransformer._lla_proj
    lonlat_argunsoft_proj = TopoCoordTransformer._lla_argunsoft_proj

    lon = 20
    lat = 50
    alt = 1000



    # print(x2 - x1, y2 - y1, z2 - z1)

    # print(pyproj.transform(lonlat_proj, lonlat_argunsoft_proj, lon, lat, alt))
    # print(lonlat_argunsoft_proj.srs)

    print(TopoCoordTransformer.lonlatalt_argunsoft_to_wgs(lon, lat, alt))
    print(TopoCoordTransformer.lonlatalt_wgs_to_argunsoft(lon, lat, alt))
    # lat_stand = 40
    # lon_stand = 50
    #
    # lat = 55
    # lon = 42  # degs
    # z_abovesea = 500  # m
    #
    # topo_transformer = TopoCoordTransformer(lat_stand=40, lon_stand=lon_stand, z_abovesea_stand=z_abovesea)
    #
    # x_topo, y_topo, z_topo = topo_transformer.lonlatalt_to_xyz_topo(lat, lon, z_abovesea)
    #
    # lat_new, lon_new, z_abovesea_new = topo_transformer.xyz_topo_to_lonlatalt(x_topo, y_topo, z_topo)
    #
    # print(lat, lat_new)
    # print(lon, lon_new)
    # print(z_abovesea, z_abovesea_new)







    # topo_transformer = TopoCoordTransformer(lat_stand=40, lon_stand=50)
    # x, y, z = topo_transformer.lonlatalt_to_xyz_topo(lon_array=50, lat_array=40, z_abovesea_array=0)
    # print(x, y, z)
    # lon, lat, alt = topo_transformer.xyz_topo_to_lonlatalt(100e3, 0, 0)
    # print(lon, lat, alt)
    #
    # topo_transformer = TopoCoordTransformer(lat_stand=0, lon_stand=0)
    # x_topo, y_topo, z_topo = topo_transformer.xyz_geocent_to_xyz_topo(6400, 0, 0)
    # print(x_topo, y_topo, z_topo)

# if __name__ == "__main__":
#     lon_array = [-1, 0, 1]
#     lat_array = [0, 0, 0]
#     z_abovesea = [100, 500, 900]
#
#     x, y, z = lonlatz_to_ecef(lon_array, lat_array, z_abovesea)
#     print(x, y, z)
#     print(np.linalg.norm([x[1] - x[0], y[1] - y[0], z[1] - z[0]]))


# if __name__== "__main__":
#     x_min = -160e3
#     x_max = 160e3
#     n_x = 640
#
#     y_min = -120e3
#     y_max = 120e3
#     n_y = 480
#
#     x_grid = np.linspace(x_min, x_max, n_x)
#     y_grid = np.linspace(y_min, y_max, n_y)
#     x_mesh, y_mesh = np.meshgrid(x_grid, y_grid)
#
#     lat_stand = 40
#     lon_stand = 20
#
#
#     _, _, z_mesh = distances_to_sealevel(lat_stand, lon_stand, x_mesh, y_mesh)
#
#     plt.imshow(z_mesh)
#     plt.show()
