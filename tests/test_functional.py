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
            "params": {
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
            "layers": [{
                "type": "wms",
                "url": "https://geo.onroerenderfgoed.be/geoserver/wms?",
                "layers": "vioe_geoportaal:onbestaande_laag"

            }]
        }

    def _get_params1(self):
        return {
            "params": {
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
            "layers": [ {
                "type": "text",
                "text": "This is a test",
                "color": "#FF3366",
                "borderwidth": 1,
                "font_size": 24,
                "text_color": "#FF3366"
            }]
        }

    def _get_params(self):
        return {
            "params": {
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

                    "type": "text",
                    "text": "This is a test",
                    "color": "#FF3366",
                    "borderwidth": 1,
                    "font_size": 24,
                    "text_color": "#FF3366"

                },
                {

                    "type": "logo",
                    "url": "https://www.onroerenderfgoed.be/assets/img/logo-og.png",
                    "opacity": 0.5

                },
                {

                    "type": "wkt",
                    "wkt": "POLYGON ((155000 215000, 160000 210000, 160000 215000, 155000 215000))",
                    "color": "steelblue",
                    "opacity": 0.5

                },
                {

                    "type": "wms",
                    "url": "https://geo.onroerenderfgoed.be/geoserver/wms?",
                    "layers": "vioe_geoportaal:landschapsbeheersplannen"

                },
                {

                    "type": "wms",
                    "url": "http://geo.api.agiv.be/geodiensten/raadpleegdiensten/GRB-basiskaart/wmsgr?",
                    "layers": "GRB_BSK"
                }

            ]
        }

    def test_map(self):
        res = self.testapp.post('/maps', json.dumps(self._get_params1()),
                                headers={'Accept': 'application/json'})
        self.assertIn('image/png', res.headers['Content-Type'])
        self.assertEqual('200 OK', res.status)

    def test_notfound(self):
        try:
            res = self.testapp.post('/notfound', json.dumps(self._get_params()), headers={'Accept': 'application/json'})
        except Exception as e:
            self.assertIsInstance(e, AppError)
        pass

    def test_renderror(self):
        data = json.dumps(self._get_params_non_existent())
        self.assertRaises(Exception, self.testapp.post, '/maps', data, headers={'Accept': 'application/json'})

    def test_validationerror(self):
        self.assertRaises(Exception, self.testapp.post, '/maps', "{}", headers={'Accept': 'application/json'})
