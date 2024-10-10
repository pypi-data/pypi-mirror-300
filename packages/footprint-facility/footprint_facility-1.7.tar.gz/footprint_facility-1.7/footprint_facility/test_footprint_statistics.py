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
import shapely
from shapely import wkt
from shapely.geometry import shape

import footprint_facility
from . import set_precision, rework_to_polygon_geometry, AlreadyReworkedPolygon

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
        stats = FootprintStatistics(fp, footprint_facility.simplify(
            fp, tolerance=0.5, tolerance_in_meter=False))
        self.assertEqual(stats.origin_points(), 7)
        self.assertEqual(stats.reworked_points(), 6)
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
        stats = _compute_simplify(
            fp, tolerance=10.0, tolerance_in_meter=False)
        self.assertEqual(stats.tolerance, 10.0)
        self.assertEqual(stats.origin_points(), 12)
        self.assertEqual(stats.reworked_points(), 11)
        self.assertTrue(isinstance(stats.map(), folium.Map))

        stats = _compute_convex_hull(fp)
        self.assertEqual(stats.origin_points(), 12)
        self.assertEqual(stats.reworked_points(), 11)
        self.assertTrue(isinstance(stats.map(), folium.Map))

        poly_simple = fp.geoms[0]
        stats = _compute_convex_hull(poly_simple)
        self.assertEqual(stats.origin_points(), 7)
        self.assertEqual(stats.reworked_points(), 6)
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

        stats = _compute_simplify(fp, tolerance=10.0, tolerance_in_meter=False)
        _geojson = stats.to_geojson()
        for feature in _geojson:
            self.assertTrue(geojson.Feature(feature).is_valid)

        stats = _compute_convex_hull(fp)
        _geojson = stats.to_geojson()
        for feature in _geojson:
            self.assertTrue(geojson.Feature(feature).is_valid)

    def test_conversion_coordinates(self):
        _wkt = """POLYGON((75.58244101140099 -85.29943099459616, 66.5853
        -85.0811, 46.7204 -83.1675, 36.0471 -80.8235, 29.6757 -78.3048,
        25.456 -75.7029, 22.4275 -73.0557, 20.1175 -70.3808, 18.2714
        -67.6878, 16.7404 -64.9819, 15.4325 -62.2664, 14.2879 -59.5433,
        13.266 -56.8141, 12.3381 -54.0796, 11.4837 -51.3405, 10.6874
        -48.5973, 9.93764 -45.8504, 9.22526 -43.1001, 8.54317 -40.3466,
        7.88562 -37.5902, 7.24788 -34.831, 6.62603 -32.0692, 6.01674
        -29.305, 5.41711 -26.5387, 4.82464 -23.7704, 4.23706 -21.0002,
        3.65232 -18.2286, 3.0685 -15.4556, 2.48378 -12.6815, 1.89642
        -9.90659, 1.30468 -7.13115, 0.706828 -4.35545, 0.101093 -1.57983,
        -0.51437 1.19541, -1.14151 3.9699, -1.78241 6.74326, -2.43933
        9.51511, -3.11477 12.285, -3.81149 15.0525, -4.53257 17.8171,
        -5.28156 20.5783, -6.06243 23.3354, -6.87981 26.0878, -7.73911
        28.8348, -8.64659 31.5754, -9.60971 34.3089, -10.6373 37.0339,
        -11.7401 39.7492, -12.931 42.4532, -14.2259 45.1438, -15.6443
        47.8187, -17.2107 50.4749, -18.956 53.1084, -20.9197 55.7142,
        -23.1527 58.2859, -25.7211 60.8146, -28.7407 63.3095, -32.2759
        65.7113, -36.5031 68.0184, -41.6199 70.1983, -47.8722 72.2041,
        -55.5302 73.9711, -64.8174 75.4121, -75.7446 76.4234, -87.8992
        76.9054, -100.397 76.7995, -112.195 76.1196, -122.56 74.9431,
        -131.251 73.3747, -138.378 71.514, -144.196 69.4397, -148.97 67.21,
        -152.931 64.8659, -156.259 62.4363, -159.092 59.9417, -161.536
        57.3968, -163.669 54.8122, -165.552 52.1959, -167.231 49.5539,
        -168.743 46.8906, -170.116 44.2097, -171.373 41.5139, -172.531
        38.8056, -173.607 36.0865, -174.611 33.3581, -175.554 30.6218,
        -176.444 27.8785, -177.288 25.1292, -178.092 22.3748, -178.861
        19.6159, -179.6 16.8532, -180 15.299267415730355, -180 90, 180 90,
        180 15.299267415730355, 179.688 14.0872, 178.999 11.3185, 178.33
        8.54753, 177.679 5.77478, 177.043 3.00064, 176.42 0.225521, 175.808
        -2.55022, 175.205 -5.32624, 174.61 -8.10221, 174.019 -10.8778,
        173.433 -13.6528, 172.849 -16.4268, 172.265 -19.1997, 171.679
        -21.9712, 171.09 -24.741, 170.495 -27.5089, 169.893 -30.2748,
        169.279 -33.0384, 168.652 -35.7995, 168.008 -38.558, 167.342
        -41.3137, 166.65 -44.0663, 165.925 -46.8156, 165.16 -49.5614,
        164.345 -52.3034, 163.467 -55.0411, 162.509 -57.7739, 161.447
        -60.5012, 160.25 -63.2219, 158.872 -65.9344, 157.243 -68.6363,
        155.254 -71.3237, 152.729 -73.9903, 149.351 -76.6243, 144.524
        -79.2029, 136.984 -81.6753, 123.827 -83.9119, 100.82387906202558
        -85.42641978721186, 100.8 -85.7265, 100.825 -85.9, 100.702 -85.909,
        90.8040265674998 -85.66880876800023, 75.6155 -85.8996, 75.6882
        -85.7284, 75.58244101140099 -85.29943099459616), (88.11476108761217
        -72.02536107007776, 90.5777 -71.8897, 99.0172 -70.9868, 106.583
        -69.7353, 113.21 -68.1949, 118.942 -66.4222, 123.873 -64.4652,
        128.119 -62.3629, 131.788 -60.1457, 134.979 -57.8371, 137.773
        -55.4553, 140.237 -53.0142, 142.428 -50.5246, 144.388 -47.995,
        146.156 -45.4321, 147.759 -42.841, 149.224 -40.2263, 150.568
        -37.5912, 151.81 -34.9387, 152.962 -32.2711, 154.035 -29.5905,
        155.041 -26.8985, 155.986 -24.1966, 156.878 -21.486, 157.722
        -18.7679, 158.524 -16.0431, 159.289 -13.3126, 160.019 -10.5772,
        160.719 -7.83745, 161.391 -5.09407, 162.038 -2.34762, 162.661
        0.401369, 163.265 3.15242, 163.849 5.90507, 164.415 8.65892, 164.965
        11.4136, 165.501 14.1687, 166.022 16.924, 166.531 19.6791, 167.028
        22.4339, 167.514 25.1879, 167.989 27.9411, 168.454 30.6933, 168.91
        33.4442, 169.357 36.1937, 169.795 38.9418, 170.224 41.6883, 170.646
        44.4331, 171.058 47.1763, 171.462 49.9177, 171.857 52.6574, 172.242
        55.3954, 172.616 58.1317, 172.977 60.8664, 173.322 63.5996, 173.648
        66.3312, 173.948 69.0614, 174.213 71.7903, 174.423 74.518, 174.547
        77.2444, 174.516 79.9695, 174.157 82.693, 172.888 85.413, 166.781
        88.1169, 20.3724 89.0493, 4.29171 86.3786, 2.25149 83.6613, 1.68051
        80.9387, 1.56185 78.2142, 1.64156 75.4883, 1.82645 72.7612, 2.07425
        70.0328, 2.36316 67.3032, 2.68373 64.5486, 3.02299 61.8161, 3.37891
        59.0822, 3.74844 56.3466, 4.12959 53.6094, 4.521 50.8705, 4.92181
        48.1299, 5.33147 45.3876, 5.74967 42.6435, 6.17631 39.8979, 6.61142
        37.1506, 7.05516 34.4018, 7.5078 31.6517, 7.96971 28.9002, 8.44135
        26.1477, 8.92326 23.3942, 9.41609 20.64, 9.92058 17.8853, 10.4375
        15.1304, 10.968 12.3755, 11.5129 9.62091, 12.0734 6.86705, 12.6511
        4.11426, 13.2472 1.36292, 13.8636 -1.38652, 14.5022 -4.13359,
        15.165 -6.8778, 15.8547 -9.61856, 16.5739 -12.3553, 17.3258
        -15.0873, 18.1142 -17.8139, 18.9432 -20.5341, 19.8177 -23.2472,
        20.7433 -25.952, 21.7265 -28.6474, 22.7752 -31.332, 23.8983
        -34.0041, 25.1067 -36.6619, 26.4133 -39.3032, 27.8333 -41.9253,
        29.3854 -44.5249, 31.0922 -47.0982, 32.9811 -49.64, 35.086 -52.1444,
        37.4483 -54.6035, 40.1192 -57.0075, 43.1618 -59.3436, 46.6526
        -61.5953, 50.6834 -63.7411, 55.3608 -65.7531, 60.7981 -67.5957,
        67.1017 -69.2238, 74.3385 -70.5836, 82.4869 -71.616,
        88.11476108761217 -72.02536107007776))"""

        geometry = wkt.loads(_wkt)
        set_precision(0.01)
        try:
            geometry = rework_to_polygon_geometry(geometry)
        except AlreadyReworkedPolygon:
            pass
        orig_count = shapely.count_coordinates(geometry)
        print(f'Number on point in original: {orig_count}')
        simpled = footprint_facility.simplify(
            geometry, tolerance=10000, tolerance_in_meter=True)
        simpled_count = shapely.count_coordinates(simpled)
        print(f'Simplified with 10km tolerance: {simpled_count}')

        simpled = footprint_facility.simplify(
            geometry, tolerance=20000, tolerance_in_meter=True)
        simpled_count = shapely.count_coordinates(simpled)
        print(f'Simplified with 20km tolerance: {simpled_count}')

        simpled = footprint_facility.simplify(
            geometry, tolerance=50000, tolerance_in_meter=True)
        simpled_count = shapely.count_coordinates(simpled)
        print(f'Simplified with 50km tolerance: {simpled_count}')

        simpled = footprint_facility.simplify(
            geometry, tolerance=100000, tolerance_in_meter=True)
        simpled_count = shapely.count_coordinates(simpled)
        print(f'Simplified with 100km tolerance: {simpled_count}')

        simpled = footprint_facility.simplify(
            geometry, tolerance=150000, tolerance_in_meter=True)
        simpled_count = shapely.count_coordinates(simpled)
        print(f'Simplified with 150km tolerance: {simpled_count}')

        simpled = footprint_facility.simplify(
            geometry, tolerance=200000, tolerance_in_meter=True)
        simpled_count = shapely.count_coordinates(simpled)
        print(f'Simplified with 200km tolerance: {simpled_count}')

        simpled = footprint_facility.simplify(
            geometry, tolerance=500000, tolerance_in_meter=True)
        simpled_count = shapely.count_coordinates(simpled)
        print(f'Simplified with 500km tolerance: {simpled_count}')

        simpled = footprint_facility.simplify(
            geometry, tolerance=1000000, tolerance_in_meter=True)
        simpled_count = shapely.count_coordinates(simpled)
        print(f'Simplified with 1000km tolerance: {simpled_count}')
