import os
import unittest
import tempdir
from wand.image import Image
from static_map_generator.renderer import Renderer, WmsRenderer, LogoRenderer, WktRenderer, TextRenderer, \
    GeojsonRenderer, ScaleRenderer, LegendRenderer, DefaultRenderer


class UtilsTests(unittest.TestCase):

    def setUp(self):
        self.tempdir = tempdir.TempDir()
        self.here = os.path.abspath(os.path.dirname(__file__))
        self.file_path = os.path.join(self.tempdir.name, 'filepath.jpg')

    def tearDown(self):
        pass

    def test_wms_renderer(self):
        renderer = Renderer.factory("wms")
        self.assertIsInstance(renderer, WmsRenderer)
        self.assertEquals(renderer.type(), "wms")

    def test_wms_renderer_errors(self):
        renderer = Renderer.factory("wms")

        with self.assertRaises(Exception) as context:
            renderer.render(
                **{
                'type': 'wms',
                'name': 'test',
                'url': 'http://non_existant/geoserver/wms?',
                'layers': 'vioe_geoportaal:onbestaande_laag',
                'filename': 'filename',
                'epsg': 31370,
                'filetype': 'png',
                'width': 500,
                'height': 500,
                'bbox': [145000, 195000, 165000, 215000]
                }
            )
        self.assertTrue(context.exception.args[0].startswith('Request could not be executed'))

        with self.assertRaises(Exception) as context:
            renderer.render(
                **{
                'type': 'wms',
                'name': 'test',
                'url': 'https://geo.onroerenderfgoed.be/geoserver/wee_em_es?',
                'layers': 'vioe_geoportaal:onbestaande_laag',
                'filename': 'filename',
                'epsg': 31370,
                'filetype': 'png',
                'width': 500,
                'height': 500,
                'bbox': [145000, 195000, 165000, 215000]
                }
            )
        self.assertTrue(context.exception.args[0].startswith('Service not found (status_code 404)'))

        with self.assertRaises(Exception) as context:
            renderer.render(
                **{
                'type': 'wms',
                'name': 'test',
                'url': 'https://geo.onroerenderfgoed.be/geoserver/wms?',
                'layers': 'vioe_geoportaal:onbestaande_laag',
                'filename': 'filename',
                'epsg': 31370,
                'filetype': 'png',
                'width': 500,
                'height': 500,
                'bbox': [145000, 195000, 165000, 215000]
                }
            )
        self.assertTrue(context.exception.args[0].startswith('Exception occured'))

    def test_text_renderer(self):
        renderer = Renderer.factory("text")
        self.assertIsInstance(renderer, TextRenderer)
        self.assertEquals(renderer.type(), "text")

    def test_wkt_renderer(self):
        renderer = Renderer.factory("wkt")
        self.assertIsInstance(renderer, WktRenderer)
        self.assertEquals(renderer.type(), "wkt")

    def test_logo_renderer(self):
        renderer = Renderer.factory("logo")
        self.assertIsInstance(renderer, LogoRenderer)
        self.assertEquals(renderer.type(), "logo")

    def test_logo_renderer_render(self):
        renderer = Renderer.factory("logo")
        renderer.render(
            **{
            'type': 'logo',
            'name': 'logo.png',
            'path': os.path.join(self.here, 'logo.png'),
            'opacity': 0.5,
            'filename': self.file_path,
            'epsg': 31370,
            'filetype': 'png',
            'width': 500,
            'height': 500,
            'bbox': [145000, 195000, 165000, 215000]
         }
        )
        self.assertTrue(os.path.isfile(self.file_path))
        image = Image(filename=self.file_path)
        self.assertIsInstance(image, Image)

    def test_geojson_renderer(self):
        renderer = Renderer.factory("geojson")
        self.assertIsInstance(renderer, GeojsonRenderer)
        self.assertEquals(renderer.type(), "geojson")
        self.assertRaises(NotImplementedError, renderer.render)

    def test_scale_renderer(self):
        renderer = Renderer.factory("scale")
        self.assertIsInstance(renderer, ScaleRenderer)
        self.assertEquals(renderer.type(), "scale")
        self.assertRaises(NotImplementedError, renderer.render)

    def test_legend_renderer(self):
        renderer = Renderer.factory("legend")
        self.assertIsInstance(renderer, LegendRenderer)
        self.assertEquals(renderer.type(), "legend")
        self.assertRaises(NotImplementedError, renderer.render)

    def test_default_renderer(self):
        renderer = Renderer.factory("")
        self.assertIsInstance(renderer, DefaultRenderer)
        self.assertEquals(renderer.type(), "default")
        self.assertRaises(NotImplementedError, renderer.render)