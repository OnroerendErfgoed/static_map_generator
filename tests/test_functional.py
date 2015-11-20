import os, unittest, json

import pytest

from paste.deploy.loadwsgi import appconfig

from pyramid import testing
from webtest import TestApp, AppError

from static_map_generator import main

TEST_DIR = os.path.dirname(__file__)
settings = appconfig(
    'config:' + os.path.join(TEST_DIR, 'test.ini'),
    name='static_map_generator'
)

class FunctionalTests(unittest.TestCase):
    def setUp(self):
        self.app = main({}, **settings)
        self.testapp = TestApp(self.app)

    def tearDown(self):
        del self.testapp, self.app
        testing.tearDown()


class RestFunctionalTests(FunctionalTests):

    def _get_params_non_existent(self):
          return {
            "layer": {
                "type": "wms",
                "name": "ONBESTAAND",
                "url": "https://geo.onroerenderfgoed.be/geoserver/wms?",
                "layers": "vioe_geoportaal:onbestaande_laag"
            }
        }

    def _get_params(self):
        return {
    "params": {
        # "filename": "file_path",
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
                "name": "GRB",
                "url": "http://geo.api.agiv.be/geodiensten/raadpleegdiensten/GRB-basiskaart/wmsgr?",
                "layers": "GRB_BSK"
            }
        }
    ]
}

    def test_map(self):
        res = self.testapp.post('/maps', json.dumps(self._get_params()),
                                headers={'Accept': 'application/json'})
        self.assertIn('image/png', res.headers['Content-Type'])
        self.assertEqual('200 OK', res.status)

    def test_notfound(self):
        try:
            res = self.testapp.post('/notfound', json.dumps(self._get_params()),headers={'Accept': 'application/json'})
        except Exception as e:
            self.assertIsInstance(e, AppError)
        pass


    def test_badrequest(self):
        try:
            res = self.testapp.post('/maps', json.dumps({'bla':'bla'}),headers={'Accept': 'application/json'})
        except Exception as e:
            self.assertIsInstance(e, AppError)
        pass