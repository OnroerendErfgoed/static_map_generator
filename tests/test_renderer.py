import unittest
from static_map_generator.renderer import Renderer, WmsRenderer, LogoRenderer, WktRenderer, TextRenderer


class UtilsTests(unittest.TestCase):

    def test_factory(self):
        self.assertIsInstance(Renderer.factory("wms"), WmsRenderer)
        self.assertIsInstance(Renderer.factory("text"), TextRenderer)
        self.assertIsInstance(Renderer.factory("wkt"), WktRenderer)
        self.assertIsInstance(Renderer.factory("logo"),  LogoRenderer)