import os
import unittest
import tempdir
# from wand.color import Color
# from wand.display import display
# from wand.image import Image
from static_map_generator.utils import merge_dicts
# from static_map_generator.utils import convert_filetype, combine_layers, convert_geojson_to_wkt, \
#     convert_wkt_to_geojson, position_figure, define_scale_number


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

    # def test_convert_filetype(self):
    #     file_path = os.path.join(self.tempdir.name, 'filepath.jpg')
    #     convert_filetype(os.path.join(self.here, "fixtures/31370.png"), file_path, 'jpg')
    #     self.assertTrue(os.path.isfile(file_path))
    #     image = Image(filename=file_path)
    #     self.assertIsInstance(image, Image)
    #     self.assertEquals(image.mimetype, 'image/jpeg')
    #
    # def test_combine_images(self):
    #     file_path = os.path.join(self.tempdir.name, 'filename.png')
    #     images = [os.path.join(self.here, "fixtures/31370.png"), os.path.join(self.here, "fixtures/4326.png")]
    #     combine_layers(images, file_path)
    #     self.assertTrue(os.path.isfile(file_path))
    #     image = Image(filename=file_path)
    #     self.assertIsInstance(image, Image)
    #
    # def test_convert_wkt_geojson(self):
    #     g1 = {"type": "MultiPoint", "coordinates": [[10, 40], [40, 30], [20, 20], [30, 10]]}
    #     print (g1)
    #     wkt1 = convert_geojson_to_wkt(g1)
    #     self.assertIsInstance(wkt1,str)
    #     print(wkt1)
    #     g2 =convert_wkt_to_geojson(wkt1)
    #     print (g2)
    #     self.assertIsInstance(g2, dict)
    #     wkt2 = convert_geojson_to_wkt(g1)
    #     self.assertEqual(wkt1, wkt2)
    #
    # def test_position_figure(self):
    #     file_path = os.path.join(self.tempdir.name, 'position.png')
    #     with Image(width=200, height=100, background=Color('red')) as img:
    #         position_figure(500, 500, img, 'center','0,0', file_path)
    #         position_figure(500, 500, img, 'north_west','0,0', file_path)
    #         position_figure(500, 500, img, 'north_east','0,0', file_path)
    #         position_figure(500, 500, img, 'south_west','0,0', file_path)
    #         position_figure(500, 500, img, 'south_east','0,0', file_path)
    #
    # def test_define_scale_number(self):
    #     print(define_scale_number(10000, 500, 150))
    #     print(define_scale_number(1000, 200, 150))
    #     print(define_scale_number(100000, 750, 150))
    #     print(define_scale_number(10000, 500, 100))
    #     print(define_scale_number(10000, 611, 150))
    #     print(define_scale_number(10000, 245, 150))
    #     print(define_scale_number(10000, 1000, 150))



