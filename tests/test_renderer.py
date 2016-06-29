import os
import unittest
import tempdir
from paste.deploy import appconfig
from wand.image import Image
from static_map_generator.renderer import Renderer, WmsRenderer, LogoRenderer, WktRenderer, TextRenderer, \
    GeojsonRenderer, ScaleRenderer, LegendRenderer, DefaultRenderer

TEST_DIR = os.path.dirname(__file__)
settings = appconfig(
    'config:' + os.path.join(TEST_DIR, 'test.ini'),
    name='static_map_generator'
)

class UtilsTests(unittest.TestCase):

    def setUp(self):
        self.tempdir = tempdir.TempDir()
        self.here = os.path.abspath(os.path.dirname(__file__))
        self.file_path = os.path.join(self.tempdir.name, 'file.png')

    def tearDown(self):
        pass

    # def test_wms_renderer(self):
    #     renderer = Renderer.factory("wms")
    #     self.assertIsInstance(renderer, WmsRenderer)
    #     self.assertEquals(renderer.type(), "wms")
    #
    # def test_wms_renderer_errors(self):
    #     renderer = Renderer.factory("wms")
    #
    #     with self.assertRaises(Exception) as context:
    #         renderer.render(
    #             **{
    #             'type': 'wms',
    #             'url': 'http://non_existant/geoserver/wms?',
    #             'layers': 'vioe_geoportaal:onbestaande_laag',
    #             'filename': 'filename',
    #             'epsg': 31370,
    #             'filetype': 'png',
    #             'width': 500,
    #             'height': 500,
    #             'bbox': [145000, 195000, 165000, 215000]
    #             }
    #         )
    #     self.assertTrue(context.exception.args[0].startswith('Request could not be executed'))
    #
    #     with self.assertRaises(Exception) as context:
    #         renderer.render(
    #             **{
    #             'type': 'wms',
    #             'url': 'https://geo.onroerenderfgoed.be/geoserver/wee_em_es?',
    #             'layers': 'vioe_geoportaal:onbestaande_laag',
    #             'filename': 'filename',
    #             'epsg': 31370,
    #             'filetype': 'png',
    #             'width': 500,
    #             'height': 500,
    #             'bbox': [145000, 195000, 165000, 215000]
    #             }
    #         )
    #     self.assertTrue(context.exception.args[0].startswith('Service not found (status_code 404)'))
    #
    #     with self.assertRaises(Exception) as context:
    #         renderer.render(
    #             **{
    #             'type': 'wms',
    #             'url': 'https://geo.onroerenderfgoed.be/geoserver/wms?',
    #             'layers': 'vioe_geoportaal:onbestaande_laag',
    #             'filename': 'filename',
    #             'epsg': 31370,
    #             'filetype': 'png',
    #             'width': 500,
    #             'height': 500,
    #             'bbox': [145000, 195000, 165000, 215000]
    #             }
    #         )
    #     self.assertTrue(context.exception.args[0].startswith('Exception occured'))
    #
    # def test_text_renderer(self):
    #     renderer = Renderer.factory("text")
    #     self.assertIsInstance(renderer, TextRenderer)
    #     self.assertEquals(renderer.type(), "text")
    #
    # def test_wkt_renderer(self):
    #     renderer = Renderer.factory("wkt")
    #     self.assertIsInstance(renderer, WktRenderer)
    #     self.assertEquals(renderer.type(), "wkt")
    #
    # def test_logo_renderer(self):
    #     renderer = Renderer.factory("logo")
    #     self.assertIsInstance(renderer, LogoRenderer)
    #     self.assertEquals(renderer.type(), "logo")
    #
    # def test_logo_renderer_render(self):
    #     renderer = Renderer.factory("logo")
    #     renderer.render(
    #         **{
    #         'type': 'logo',
    #         'url': 'https://www.onroerenderfgoed.be/assets/img/logo-og.png',
    #         'opacity': 0.5,
    #          'imagewidth': 100,
    #          'imageheight': 100,
    #          'gravity': 'south_west',
    #         'filename': self.file_path,
    #         'epsg': 31370,
    #         'filetype': 'png',
    #         'width': 500,
    #         'height': 500,
    #         'bbox': [145000, 195000, 165000, 215000],
    #             'offset': '0,0'
    #      }
    #     )
    #     self.assertTrue(os.path.isfile(self.file_path))
    #     image = Image(filename=self.file_path)
    #     self.assertIsInstance(image, Image)
    #
    # def test_geojson_renderer(self):
    #     renderer = Renderer.factory("geojson")
    #     self.assertIsInstance(renderer, GeojsonRenderer)
    #     self.assertEquals(renderer.type(), "geojson")
    #
    # def test_multipoint_renderer_render(self):
    #     renderer = Renderer.factory("wkt")
    #     renderer.render(
    #         **{
    #         'type': 'wkt',
    #         'opacity': 0.5,
    #         'filename': self.file_path,
    #         'epsg': 31370,
    #         'filetype': 'png',
    #         'width': 500,
    #         'height': 500,
    #         'color': '#0000ff',
    #         'wkt': 'MULTIPOINT ((103500 192390.11), (103912.03 192390.11))',
    #         'bbox': [100000, 100000, 200000, 200000]
    #      }
    #     )
    #     self.assertTrue(os.path.isfile(self.file_path))
    #     image = Image(filename=self.file_path)
    #     self.assertIsInstance(image, Image)
    #
    # def test_multipoint2_renderer_render(self):
    #     renderer = Renderer.factory("wkt")
    #     renderer.render(
    #         **{
    #         'type': 'wkt',
    #         'opacity': 0.5,
    #         'filename': self.file_path,
    #         'epsg': 31370,
    #         'filetype': 'png',
    #         'width': 500,
    #         'height': 500,
    #         'color': '#0000ff',
    #         'wkt': 'MULTIPOINT (103500 192390.11, 103912.03 192390.11)',
    #         'bbox': [100000, 100000, 200000, 200000]
    #      }
    #     )
    #     self.assertTrue(os.path.isfile(self.file_path))
    #     image = Image(filename=self.file_path)
    #     self.assertIsInstance(image, Image)
    #
    # def test_geojson_renderer_render(self):
    #     renderer = Renderer.factory("geojson")
    #     renderer.render(
    #         **{
    #         'type': 'geojson',
    #         'opacity': 0.5,
    #         'filename': self.file_path,
    #         'epsg': 31370,
    #         'filetype': 'png',
    #         'width': 500,
    #         'height': 500,
    #         'color': 'steelblue',
    #         'geojson':{
    #             "type":"MultiPolygon",
    #             "coordinates":[[[[103827.44321801752,192484.5100535322],[103826.65621839411,192565.57026445214],[103839.2000972359,192622.4958831761],[103877.27257229008,192673.1911981115],[103981.90807816133,192592.71585010737],[104050.62835409257,192535.07265175506],[104119.78606355426,192526.95860514138],[104157.5529127745,192543.1371434061],[104163.33481632298,192516.068607972],[104043.86794770884,192451.07658289373],[103839.39232099024,192304.2814310426],[103825.49962980268,192434.99411542248],[103827.44321801752,192484.5100535322]]]],
    #             "crs":{
    #             "type":"name",
    #             "properties":{
    #             "name":"urn:ogc:def:crs:EPSG::31370"}}},
    #         'bbox': [100000, 100000, 200000, 200000]
    #      }
    #     )
    #     self.assertTrue(os.path.isfile(self.file_path))
    #     image = Image(filename=self.file_path)
    #     self.assertIsInstance(image, Image)
    #
    # def test_geojson_renderer_render2(self):
    #     renderer = Renderer.factory("geojson")
    #     renderer.render(
    #         **{
    #         'type': 'geojson',
    #         'opacity': 0.5,
    #         'filename': self.file_path,
    #         'epsg': 31370,
    #         'filetype': 'png',
    #         'width': 500,
    #         'height': 500,
    #         'color': 'steelblue',
    #         'geojson':{'crs': {'type': 'name', 'properties': {'name': 'EPSG:31370'}}, 'type': 'MultiPoint', 'coordinates': [[103912.03, 192390.11],[103500, 192390.11]]},
    #         'bbox': [100000, 100000, 200000, 200000]
    #      }
    #     )
    #     self.assertTrue(os.path.isfile(self.file_path))
    #     image = Image(filename=self.file_path)
    #     self.assertIsInstance(image, Image)
    #
    # def test_scale_renderer(self):
    #     renderer = Renderer.factory("scale")
    #     renderer.render(
    #         **{
    #         'type': 'scale',
    #          'gravity': 'south_west',
    #          'offset':'10,20',
    #          'opacity': 1,
    #         'filename': self.file_path,
    #         'epsg': 31370,
    #         'filetype': 'png',
    #         'width': 750,
    #         'height': 750,
    #         'bbox': [100000, 100000, 200000, 200000],
    #         'font_size': 11,
    #         'imagewidth': 200,
    #         'imageheight': 50
    #      })
    #     self.assertIsInstance(renderer, ScaleRenderer)
    #     self.assertEquals(renderer.type(), "scale")
    #     self.assertTrue(os.path.isfile(self.file_path))
    #     image = Image(filename=self.file_path)
    #     self.assertIsInstance(image, Image)
    #
    # def test_legend_renderer(self):
    #     renderer = Renderer.factory("legend")
    #     self.assertIsInstance(renderer, LegendRenderer)
    #     self.assertEquals(renderer.type(), "legend")
    #     self.assertRaises(NotImplementedError, renderer.render)
    #
    #
    # def test_default_renderer(self):
    #     renderer = Renderer.factory("")
    #     self.assertIsInstance(renderer, DefaultRenderer)
    #     self.assertEquals(renderer.type(), "default")
    #     self.assertRaises(NotImplementedError, renderer.render)