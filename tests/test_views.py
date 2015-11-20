import unittest

from pyramid import testing
from pyramid.httpexceptions import HTTPBadRequest

try:
    from unittest.mock import Mock, patch
except:
    from mock import Mock, patch


def _registerRoutes(config):
    config.add_route('maps', '/maps')
    config.add_route('home', '/')
    settings = {
    }
    config.registry.settings = settings


class ViewTests(unittest.TestCase):
    def setUp(self):
        self.request = testing.DummyRequest()
        self.config = testing.setUp(request=self.request)
        _registerRoutes(self.config)

    def tearDown(self):
        testing.tearDown()


class RestViewTests(ViewTests):
    def _get_params(self):
        return {
    "params": {
        "filename": "file_path",
        "epsg": 31370,
        "filetype": "png",
        "width": 500,
        "height": 500,
        "bbox": [
            145000,
            195000,
            165000,
            215000
        ]
    },
    "layers": [
        {
            "layer": {
                "type": "text",
                "name": "text.png",
                "text": "This is a test",
                "color": "#FF3366",
                "borderwidth": 1,
                "font_size": 24,
                "text_color": "#FF3366"
            }
        },
        {
            "layer": {
                "type": "logo",
                "name": "logo.png",
                "path": "logo.png",
                "opacity": 0.5
            }
        },
        {
            "layer": {
                "type": "wkt",
                "name": "WKT",
                "wkt": "POLYGON ((155000 215000, 160000 210000, 160000 215000, 155000 215000))",
                "color": "steelblue",
                "opacity": 0.5
            }
        },
        {
            "layer": {
                "type": "wms",
                "name": "OE",
                "url": "https://geo.onroerenderfgoed.be/geoserver/wms?",
                "layers": "vioe_geoportaal:landschapsbeheersplannen",
                "featureid": "landschapsbeheersplannen.3816"
            }
        },
        {
            "layer": {
                "type": "wms",
                "name": "ONBESTAAND",
                "url": "https://geo.onroerenderfgoed.be/geoserver/wms?",
                "layers": "vioe_geoportaal:onbestaande_laag"
            }
        },
        {
            "layer": {
                "type": "wms",
                "name": "GRB",
                "url": "http://geo.api.agiv.be/geodiensten/raadpleegdiensten/GRB-basiskaart/wmsgr?",
                "layers": "GRB_BSK"
            }
        }
    ]
}

    def _get_rest_view(self, request):
        from static_map_generator.views.views import RestView

        return RestView(request)

    def test_home(self):
        from static_map_generator.views.views import RestView

        homeview = RestView(self.request)
        home = homeview.home()
        self.assertEqual('200 OK', home.status)

    def test_nojson(self):
        from static_map_generator.views.views import RestView

        rv = RestView(self.request)
        self.assertRaises(HTTPBadRequest, rv.maps_by_post)

    def test_notfound(self):
        from static_map_generator.views.exceptions import not_found
        rv = not_found(self.request)
        self.assertIsInstance(rv,dict)
        self.assertEquals(rv['message'], 'De door u gevraagde resource kon niet gevonden worden.')
