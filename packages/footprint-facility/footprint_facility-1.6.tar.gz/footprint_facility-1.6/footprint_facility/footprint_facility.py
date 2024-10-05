"""
   Copyright 2024 - GAEL Systems

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

     http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""
import time
import uuid
import logging
from functools import wraps
from operator import ge

import geojson
import numpy as np
import shapely
from pyproj import Transformer
from shapely import Geometry, Point
from shapely.geometry.base import BaseMultipartGeometry
from shapely.ops import transform as sh_transform

'''
Checks the singularities in the footprints
 - longitude/antimeridian : when the footprint crosses ±180 meridian
 - polar : when the footprint contains polar area (also ±180 meridian)
'''

# Global Time variables
_enable_time = False
_incremental_time = False
_summary_time = True
_summaries = {}

_raise_exception = True

# Footprint precision coordinates
_precision = 0


logger = logging.getLogger('footprint_facility')


class AlreadyReworkedPolygon(Exception):
    pass


def set_precision(precision: float):
    global _precision
    if precision < 0:
        raise ValueError("precision shall be greater than 0")
    _precision = precision


def get_precision() -> float:
    global _precision
    return _precision


def set_raise_exception(flag=True):
    global _raise_exception
    _raise_exception = flag


def check_time(enable=True, incremental=False, summary_time=True):
    global _enable_time, _incremental_time, _summary_time
    _enable_time = enable
    _incremental_time = incremental
    _summary_time = summary_time
    if not _incremental_time and not _summary_time:
        _enable_time = False


def show_summary():
    global _summaries
    for key in _summaries.keys():
        count_point = 0
        count_cpu_time = 0
        for summary in _summaries[key]:
            count_point = (count_point +
                           shapely.count_coordinates(summary['args'][0])) \
                if shapely.is_geometry(summary['args'][0]) else 0
            count_cpu_time = count_cpu_time + summary['cpu_time_ns']
        logger.info(
            f"{key}:\t{count_cpu_time / count_point / 1000:.2f} μs/point")


def timing(f):
    @wraps(f)
    def inner_timer_function(*args, **kw):
        global _enable_time, _incremental_time, _summary_time, _summaries
        if _enable_time:
            ts = time.perf_counter(), time.process_time_ns()
            result = f(*args, **kw)
            te = time.perf_counter(), time.process_time_ns()
            if _incremental_time:
                logger.info('func:%r args:[%r, %r] took: %2.4f ns' %
                            (f.__name__, args, kw, te[1] - ts[1]))
            if _summary_time:
                if not _summaries.get(f.__name__):
                    _summaries[f.__name__] = []

                _summaries[f.__name__].append({
                    'args': args, 'real_time': te[0] - ts[0],
                    'cpu_time_ns': te[1] - ts[1]})
        else:
            result = f(*args, **kw)
        return result

    return inner_timer_function


def exception_handler(func):
    def inner_exception_function(*args, **kwargs):
        global _raise_exception
        if not _raise_exception:
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logger.warning(
                    f"{func.__name__} Cannot manage footprint ({str(e)})")
                return args[0]
        else:
            return func(*args, **kwargs)
    return inner_exception_function


def precision_handler(func):
    def inner_precision_function(*args, **kwargs):
        if get_precision() > 0:
            ''' WARN: https://github.com/shapely/shapely/issues/1952
            Issue #1952 set_precision() changes order of coordinates.

            The issue discussion describe the internal convention the
            coordinates of exterior rings follow a clockwise orientation and
            interior rings have a counter-clockwise orientation. This is the
            opposite of the OGC specifications because the choice was made
            before this was included in the standard.
            The starting point of rings and the order of geometry types in a
            collection can be changed, but the result is undefined. When
            :func:`~shapely.normalize` is used though, it will make sure that
            the starting point of rings is lower left and that collections are
            ordered by geometry type.

            In the footprint representation primary analysis we highlighted
            the coordinates order have not impact wrt its representation and
            search processes.
            Let's wait and see the evolution of the library and possible issue
            reported here if any.
            '''
            return shapely.set_precision(
                func(*args, **kwargs),
                grid_size=get_precision())
        else:
            return func(*args, **kwargs)
    return inner_precision_function


################################
# Prepare projection transformers
# Objective is to use metric projection centered on the concerned polar
# point to avoid polar discontinuity.
# Projection user: polar stereoscopic epsg:3031
wgs84_to_polar_north = Transformer.from_crs(
    "+proj=longlat +datum=WGS84 +no_defs",
    "+proj=stere +lat_0=90 +lat_ts=75").transform
wgs84_to_polar_south = Transformer.from_crs(
    "+proj=longlat +datum=WGS84 +no_defs",
    "+proj=stere +lat_0=-90 +lat_ts=-75").transform
north_pole_m = sh_transform(wgs84_to_polar_north, Point(float(0), float(90)))
south_pole_m = sh_transform(wgs84_to_polar_south, Point(float(0), float(-90)))


@timing
def check_cross_antimeridian(geometry: Geometry) -> bool:
    """
    Checks if the geometry pass over ±180 longitude position.
    The detection of antimeridian is performed according to the distance
    between longitudes positions between consecutive points of the geometry
    points. The distance shall be greater than 180 to avoid revert longitude
    signs around greenwich meridian 0.
    It is also considered crossing antimeridian when one of the polygon
    longitude is exactly to +-180 degrees.
    :parameter geometry: The geometry to be controlled.
    :return: True if the geometry pass over antimeridian, False otherwise.
    """
    # Case of Collection of geometries (i.e. Multipolygons)
    if hasattr(geometry, "geoms"):
        for geom in geometry.geoms:
            if check_cross_antimeridian(geom):
                return True
        return False
    # Path of points shall exist (Polygon or Linestring)
    boundary = np.array(shapely.get_coordinates(geometry))
    i = 0
    while i < boundary.shape[0] - 1:
        if (boundary[i, 0] == 180 or boundary[i, 0] == -180
                or abs(boundary[i + 1, 0] - boundary[i, 0]) > 180):
            return True
        i = i + 1
    return False


def _check_contains_north_pole(geometry: Geometry):
    """
    Check if the given geometry contains North Pole.
    Warning: the re-projection process does not work properly when coordinates
    of the geometry pass over antimeridian. This method cannot be used without
    applying the polar inclusive method as implemented in
    `rework_to_polygon_geometry`.

    See comment on globals variable for projection details.

    :parameter geometry: the complex reference geometry.
    :return: True if the given geometry contains North Pole
    """
    north = shapely.intersection(
        shapely.box(-180, 0, 180, 90),
        shapely.buffer(geometry, 0))

    geometry_m = sh_transform(wgs84_to_polar_north, north)
    # Use 1m larger as rounded to handle float values inaccuracies.
    geometry_m = geometry_m.buffer(1)

    return geometry_m.contains(north_pole_m)


def _check_contains_south_pole(geometry: Geometry):
    """
    Check if the given geometry contains South Pole.
    Warning: the re-projection process does not work properly when coordinates
    of the geometry pass over antimeridian. This method cannot be used without
    applying the polar inclusive method as implemented in
    `rework_to_polygon_geometry`.

    See comment on globals variable for projection details.

    :parameter geometry: the complex reference geometry.
    :return: True if the given geometry contains South Pole
    """

    south = shapely.intersection(
        shapely.box(-180, -90, 180, 0),
        shapely.buffer(geometry, 0))

    geometry_m = sh_transform(wgs84_to_polar_south, south)
    # Use 1m larger as rounded to handle float values inaccuracies.
    geometry_m = geometry_m.buffer(1)

    return geometry_m.contains(south_pole_m)


def poly_to_point(polygon: shapely.Polygon):
    boundaries = shapely.get_coordinates(polygon)
    return shapely.multipoints(boundaries)


def _check_contains_pole(geometry: Geometry) -> bool:
    """
    Checks if the geometry pass over the North or South Pole.
    WARN: this method shall be used only once improved geometry with inclusion
    of polar point.
    :parameter geometry: the geometry to be controlled.
    :return: True if the geometry contains polar point, False otherwise.
    """
    return (_check_contains_north_pole(geometry) or
            _check_contains_south_pole(geometry))


def _plus360(x):
    """
    Translate to +360 degrees the x longitude value when value is negative.

    Note: The translation is only applicable to longitude values with unit
    in degrees. It shall be efficient when previous coordinate longitude is
    180 degrees far from this point.

    :param x: the longitude to be translated
    :return:  the shifted longitude when required.
    """
    if x < 0:
        x = x + 360
    return x


def _polynom_coefficients(px1, py1, px2, py2):
    """
    Resolves the linear equation passing by given p1 and p2 coordinates.
    :return: Two values: first is the leading coefficient (m) second is the
    constant coefficient (b) that can be used as Y=m.X+b
    """
    if px2 - px1 == 0:
        raise AlreadyReworkedPolygon(
            "Points are aligned onto the antimeridian")
    # leading coefficient
    m = (py2 - py1) / (px2 - px1)
    # retrieves b
    b = py1 - m * px1
    return m, b


def _lat_cross_antimeridian(p1, p2):
    """
      Retrieves the latitude position in the line drawn by 2
      point parameters p1 and p2 and crossing ±180 longitude.
    """
    x1 = _plus360(p1[0])
    y1 = p1[1]

    x2 = _plus360(p2[0])
    y2 = p2[1]

    m, b = _polynom_coefficients(x1, y1, x2, y2)
    # resolve polynom with x=180
    return 180.0 * m + b


def _split_polygon_to_antimeridian(geometry: Geometry):
    """
    This method splits geometry among the antimeridan area. It removes link
    to the pole if any.
    :param geometry: the geometry to split
    :return: polygon or multipolygon if the geometry requires to be split.
    """
    if not check_cross_antimeridian(geometry):
        return geometry

    boundaries = np.array(shapely.get_coordinates(geometry))

    left_antimeridian = []
    right_antimeridian = []
    polygons = [right_antimeridian, left_antimeridian]

    hsign = 0 if boundaries[0, 0] < 0 else 1
    for index, boundary in enumerate(boundaries):
        if (index < boundaries.shape[0]-1 and
                abs(boundaries[index + 1, 0] - boundaries[index, 0]) > 180):
            hsign = 0 if boundaries[index+1, 0] < 0 else 1

        if ((boundary[0] == -180 or boundary[0] == 180) and
                (boundary[1] == -90 or boundary[1] == 90)):
            continue
        polygons[hsign].append(boundary)

    # Checks the empty list if any
    if not left_antimeridian and not right_antimeridian:
        raise ValueError("Footprint cannot be split across the antimeridian")
    elif not left_antimeridian:
        reworked = shapely.polygons(right_antimeridian)
    elif not right_antimeridian:
        reworked = shapely.polygons(left_antimeridian)
    else:
        reworked = shapely.multipolygons([
            shapely.polygons(left_antimeridian),
            shapely.polygons(right_antimeridian)])

    return reworked


def _to_polygons(geometries):
    for geometry in geometries:
        if isinstance(geometry, shapely.Polygon):
            yield geometry
        else:
            yield from geometry.geoms


def check_cross_equator(geometry: Geometry):
    boundaries = np.array(shapely.get_coordinates(geometry))
    previous = []
    for boundary in boundaries:
        if len(previous) == 2 and ((previous[1] > 0 > boundary[1]) or (
                previous[1] < 0 < boundary[1])):
            return True
        previous = boundary
    return False


def _split_polygon_to_equator(geometry: Geometry):
    """
    Split geometry among the equator: this is useful when the footprint cover
    both hemisphere and includes overlaping with antimeridian: In this case
    both poles are included into the shape of the footprint and intersection
    method fails.
    :param geometry:
    :return:
    """
    north = shapely.intersection(
        shapely.box(-180, 0, 180, 90),
        shapely.buffer(geometry, 0))
    south = shapely.intersection(
        shapely.box(-180, -90, 180, 0),
        shapely.buffer(geometry, 0))

    return shapely.MultiPolygon(_to_polygons([north, south]))


@exception_handler
def rework_to_polygon_geometry(geometry: Geometry):
    return _rework_to_polygon_geometry(geometry)


@timing
@precision_handler
def _rework_to_polygon_geometry(geometry: Geometry):
    """Rework the geometry to manage polar and antimeridian singularity.
    This process implements the **Polar inclusive algorithm**.
    The objective of this algorithm is to add the North/South Pole into
    the list of coordinates of geometry polygon at the antimeridian cross.

    When the geometry contains the pole the single polygon geometry including
    the pole in its border point list is properly interpreted by displays
    systems. When the geometry does not contain the pole, the geometry shall be
    split among the antimeridian line.

    :param geometry: the geometry crossing the antimeridian.
    :return: the modified geometry with the closest pole included at
     antimeridian crossing.
    """
    if not check_cross_antimeridian(geometry):
        return geometry

    # Manage case of multipolygon input
    if isinstance(geometry, shapely.geometry.MultiPolygon):
        rwrk = []
        for geom in geometry.geoms:
            reworked = rework_to_polygon_geometry(geom)
            if isinstance(reworked, BaseMultipartGeometry):
                raise AlreadyReworkedPolygon(
                    "Algorithm not supported already reworked inputs.")
            rwrk.append(reworked)
        return shapely.geometry.MultiPolygon(rwrk)

    if isinstance(geometry, shapely.geometry.LineString):
        return rework_to_linestring_geometry(geometry)

    if not isinstance(geometry, shapely.geometry.Polygon):
        raise ValueError("Polygon and MultiPolygon features only are "
                         f"supported ({type(geometry).__name__})")

    boundaries = np.array(shapely.get_coordinates(geometry))
    i = 0
    vertical_set = False
    while i < boundaries.shape[0] - 1:
        if abs(boundaries[i + 1, 0] - boundaries[i, 0]) > 180:
            if not vertical_set:
                vsign = -1 if boundaries[i, 1] < 0 else 1
                vertical_set = True
            hsign = -1 if boundaries[i, 0] < 0 else 1
            lat = _lat_cross_antimeridian(boundaries[i], boundaries[i + 1])
            boundaries = np.insert(boundaries, i + 1, [
                [hsign * 180, lat], [hsign * 180,  vsign * 90],
                [-hsign * 180,  vsign * 90], [-hsign * 180, lat]
            ], axis=0)
            i += 5
        else:
            i += 1
    geometry_type = type(geometry)
    reworked = geometry_type(boundaries)

    # When the geometry does not contain pole: Cuts the geometry among the
    # antimeridian line.
    if not _check_contains_pole(reworked):
        reworked = _split_polygon_to_antimeridian(reworked)
    else:
        # Case of footprint crossing equator, antimeridian and polar zone
        # Split at the equator
        # Warn:
        if check_cross_equator(reworked):
            reworked = _split_polygon_to_equator(reworked)
        # When footprint contains overlapping, it happens at polar location.
        # Polygon containing overlapping are considered invalid in shapely
        # library. It includes validity check and correction methods.
        # The shapely correction method extrude the overlap areas and fails
        # to generate patchwork of polygons at polar area. This is probably
        # due to the antimeridian crossing.
        # Shapely "buffer" method fixe"s the geometry merging overlapping
        # regions.
        if not shapely.is_valid(reworked):
            # reworked = shapely.make_valid(reworked)
            reworked = shapely.buffer(reworked, 0)
    return reworked


@timing
@precision_handler
def rework_to_linestring_geometry(geometry: Geometry):
    """
    Elaborates linestring geometry from thin polygon and manage the
    antimeridian cross.

    :param geometry:
    :return:
    """
    boundaries = np.array(shapely.get_coordinates(geometry))
    boundaries = np.unique(boundaries.round(decimals=1), axis=0)

    if check_cross_antimeridian(geometry):
        _min = min(boundaries, key=lambda point: point[0])
        _max = max(boundaries, key=lambda point: point[0])
        lat_at_180 = _lat_cross_antimeridian(_min, _max)
        negative = [-180, lat_at_180]
        positive = [180, lat_at_180]

        left_antimeridian = []
        right_antimeridian = []
        [right_antimeridian.append(boundary)
         for boundary in boundaries if boundary[0] > 0]
        [left_antimeridian.append(boundary)
         for boundary in boundaries if boundary[0] < 0]

        right_antimeridian = np.concatenate(
            (right_antimeridian, np.array([positive])), axis=0)
        left_antimeridian = np.concatenate(
            (np.array([negative]), left_antimeridian), axis=0)

        reworked = shapely.multilinestrings([
            shapely.linestrings(left_antimeridian),
            shapely.linestrings(right_antimeridian)])
    else:
        reworked = shapely.linestrings(boundaries)

    return reworked


def _simplify_compute_statistics(geometry, tolerance=.1,
                                 preserve_topology=True):
    """
    Computes the simplified variatiopns statitics:
     - number of points change
     - area change

    :param geometry: the geometry to be computed
    :param tolerance: the ify
    :param preserve_topology:
    :return:
    """
    origin_area = getattr(geometry, 'area', 0)
    origin_points_number = len(shapely.get_coordinates(geometry))

    reworked = simplify(geometry, tolerance=tolerance,
                        preserve_topology=preserve_topology)

    new_area = reworked.area
    variation_area = (new_area - origin_area) / origin_area
    new_points_number = len(shapely.get_coordinates(reworked))
    variation_point = ((new_points_number - origin_points_number) /
                       origin_points_number)

    return {'tolerance': tolerance,
            'geometry': reworked,
            'Area': {"orig": origin_area, "new": new_area,
                     "variation": variation_area},
            'Points': {"orig": origin_points_number,
                       "new": new_points_number,
                       "variation": variation_point}}


def find_best_tolerance_for(geometry,
                            max_area_percentage_change=1,
                            min_point_number_reduction_percentage=50):
    """
    The Douglas-Peucker based #simplify algorithm requires a tolerance shall
    be parametrized. The best tolerance value depends on the geometry shape
    complexity. This method aims to evaluate the best tolerance for a
    geometry controlling its surface change wrt the reduction of the number of
    points.

    This method computes statistics by running #symplify method with various
    tolerance values. It may be time-consuming when expected values greater
    than 1% of area change and up to 80% of reduced points numbers.
    :param geometry: the geometry to evaluate
    :param max_area_percentage_change:  maximum accepted surface modification.
    :param min_point_number_reduction_percentage: point reduction percentage
       objective.
    :return: the tolerance due to the given parameters if parameters cannot
    be reached, 0 is returned.
    """
    min_tolerance = 0.0001
    max_tolerance = 2.0
    step = 0.0001

    previous_tolerance = 0

    for tolerance in (map(lambda x: x/10000.0,
                          range(int(min_tolerance*10000),
                                int(max_tolerance*10000),
                                int(step*10000)))):
        measurement = _simplify_compute_statistics(geometry, tolerance)

        # Checks surface area modification by the algorithm
        area_var = measurement['Area']['variation']
        if area_var >= abs(max_area_percentage_change / 100):
            return previous_tolerance

        # Checks coord number modification by the algorithm
        point_variation = abs(measurement['Points']['variation'])
        if point_variation >= abs(min_point_number_reduction_percentage / 100):
            return previous_tolerance

        previous_tolerance = tolerance
    return 0


@timing
@precision_handler
def simplify(geometry: Geometry, tolerance=.1, preserve_topology=True):
    """
    Returns a simplified representation of the geometric object.
    This method wraps shapely library https://shapely.readthedocs.io/en/
       stable/reference/shapely.simplify.html#shapely.simplify

    All points in the simplified object will be within the tolerance distance
    of the original geometry. default a slower algorithm is used that
    preserves topology. If preserve topology is set to False the much quicker
    Douglas-Peucker algorithm is used.

    :param geometry:
    :param tolerance: The maximum allowed geometry displacement. The higher
    this value, the smaller the number of vertices in the resulting geometry.
    :param preserve_topology: default (True), the operation will avoid
    creating invalid geometries (checking for collapses, ring-intersections,
    etc.), but this is computationally more expensive.
    :return:
    """
    _geometry = geometry
    if isinstance(geometry, shapely.geometry.Polygon):
        _geometry = shapely.buffer(geometry, 0.0)
    return shapely.simplify(_geometry, tolerance=tolerance,
                            preserve_topology=preserve_topology)


############################################################################
# Utilities for Geometry manipulation
# - convert to wkt
# - convert to geojson
# - build sample disk footprint from its center and radius.
#############################################################################
# Create WKT string from Geometry
def to_wkt(geometry: Geometry):
    """
    Convert the geometry to string WKT format
    :param geometry: the geometry to convert
    :return: the string in WKT format
    """
    return getattr(geometry, "wkt")


# Create GeoJSON string from Geometry
def to_geojson(geometry: Geometry, feature_id=None, properties=None):
    """
    Convert the geometry to string GeoJSON format. The identifier of the
    feature can be provided by the caller as well as the property dictionary.
    :param geometry: the geometry to convert
    :param feature_id: a user defined feature identifier, the identifier will
    be automatically generated if not provided by the user.
    :param properties: a set of property to embed into the feature.
    :return: the GeoJSON string
    """
    if properties is None:
        properties = {}
    if feature_id is None:
        feature_id = str(uuid.uuid4())

    feature = geojson.Feature(id=feature_id,
                              geometry=geometry,
                              properties=properties)
    features = [feature]
    return geojson.FeatureCollection(features)
