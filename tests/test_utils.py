import os
import unittest
import tempdir
from static_map_generator.utils import merge_dicts, rescale_bbox, calculate_scale


class UtilsTests(unittest.TestCase):

    def setUp(self):
        self.tempdir = tempdir.TempDir()
        self.here = os.path.abspath(os.path.dirname(__file__))

    def tearDown(self):
        pass

    def test_merge_dicts(self):
        x = {'a': 1, 'b': 2}
        y = {'b': 3, 'c': 4}
        z = merge_dicts(x, y)
        self.assertEquals(z, {'a': 1, 'b': 3, 'c': 4})

    def test_calculate_scale(self):
        scale_width, scale_label = calculate_scale(0.521, 650)
        self.assertEqual(scale_label, "60 m")
        self.assertEqual(scale_width, 115)

    def test_rescale_bbox(self):
        bbox = [1, 2, 3, 4]
        new_bbox = rescale_bbox(5, 10, bbox)
        self.assertEqual([0, 2, 4, 4], new_bbox)
        new_bbox = rescale_bbox(10, 5, bbox)
        self.assertEqual([1, 1, 3, 5], new_bbox)
        new_bbox = rescale_bbox(5, 5, bbox)
        self.assertEqual([1, 2, 3, 4], new_bbox)


