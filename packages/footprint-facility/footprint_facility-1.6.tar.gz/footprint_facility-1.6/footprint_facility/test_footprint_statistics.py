"""
   Copyright 2024 - Gael Systems

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
from unittest import TestCase

import folium
import geojson
from shapely import wkt
from shapely.geometry import shape

import footprint_facility

try:
    from .footprint_statistcs import (compute_area_from_4326,
                                      area_to_user_readable,
                                      FootprintStatistics,
                                      _compute_simplify,
                                      _compute_convex_hull)
except ImportError:
    from footprint_statistcs import (compute_area_from_4326,
                                     area_to_user_readable,
                                     FootprintStatistics,
                                     _compute_simplify,
                                     _compute_convex_hull)


#############################################################################
# Test Class
#############################################################################
class TestStatistics(TestCase):
    @classmethod
    def setUpClass(cls):
        pass

    def test_compute_area_from_4326_1(self):
        poly = wkt.loads('''\
            POLYGON ((24.8085317 46.8512821,
                24.7986952 46.8574619,
                24.8088238 46.8664741,
                24.8155239 46.8576335,
                24.8085317 46.8512821))''')

        self.assertAlmostEqual(abs(compute_area_from_4326(poly)), 1083466.869,
                               delta=1e-3)

    def test_compute_area_from_4326_2(self):
        """
        Huge sample area coming form leaflet sample
        """
        poly = wkt.loads('''\
            POLYGON((20 35, 22 34, 45 20, 30 5, 10 10, 10 30, 20 35))''')

        self.assertAlmostEqual(abs(compute_area_from_4326(poly)),
                               7_927_593_710_574.936,
                               delta=1e-3)

    def test_area_to_user_readable(self):
        value = area_to_user_readable(10_000_000)
        self.assertTrue('km<sup>2' in value)
        value = area_to_user_readable(100_000)
        self.assertTrue('m<sup>2' in value)

    def test_class_footprint_statistics(self):
        fp = wkt.loads(
            "POLYGON((20 35, 22 34, 45 20, 30 5, 10 10, 10 30, 20 35))")
        stats = FootprintStatistics(fp, footprint_facility.simplify(fp, 0.5))
        self.assertEqual(stats.origin_points(), 7)
        self.assertEqual(stats.reworked_points(), 6)
        self.assertEqual(stats.delta_point(), 1)
        self.assertTrue(isinstance(stats.map(), folium.Map))

    def test_class_simplify_statistics(self):
        fp = shape(dict(
              {
                "coordinates":
                [
                  [
                    [
                      [3.292, 47.148],
                      [5.651, 46.967],
                      [4.963, 48.912],
                      [1.887, 48.873],
                      [1.137, 46.395],
                      [3.557, 44.765],
                      [3.292, 47.148]
                    ]
                  ],
                  [
                    [
                      [7.195, 47.032],
                      [7.195, 49.461],
                      [5.844, 49.461],
                      [5.844, 47.032],
                      [7.195, 47.032]
                    ]
                  ]
                ],
                "type": "MultiPolygon"
              }))

        stats = _compute_simplify(fp, tolerance=10.0)
        self.assertEqual(stats.tolerance, 10.0)
        self.assertEqual(stats.origin_points(), 12)
        self.assertEqual(stats.reworked_points(), 11)
        self.assertEqual(stats.delta_point(), 1)
        self.assertTrue(isinstance(stats.map(), folium.Map))

        stats = _compute_convex_hull(fp)
        self.assertEqual(stats.origin_points(), 12)
        self.assertEqual(stats.reworked_points(), 11)
        self.assertEqual(stats.delta_point(), 1)
        self.assertTrue(isinstance(stats.map(), folium.Map))

    def test_class_simplify_statistics_to_geojson(self):
        fp = shape(dict(
              {
                "coordinates":
                [
                  [
                    [
                      [3.292, 47.148],
                      [5.651, 46.967],
                      [4.963, 48.912],
                      [1.887, 48.873],
                      [1.137, 46.395],
                      [3.557, 44.765],
                      [3.292, 47.148]
                    ]
                  ],
                  [
                    [
                      [7.195, 47.032],
                      [7.195, 49.461],
                      [5.844, 49.461],
                      [5.844, 47.032],
                      [7.195, 47.032]
                    ]
                  ]
                ],
                "type": "MultiPolygon"
              }))

        stats = _compute_simplify(fp, tolerance=10.0)
        _geojson = stats.to_geojson()
        for feature in _geojson:
            self.assertTrue(geojson.Feature(feature).is_valid)

        stats = _compute_convex_hull(fp)
        _geojson = stats.to_geojson()
        for feature in _geojson:
            self.assertTrue(geojson.Feature(feature).is_valid)
