import json
import os
import unittest

import responses
from paste.deploy.loadwsgi import appconfig
from pyramid import testing
from pyramid.compat import text_
from webtest import TestApp

from static_map_generator import main

TEST_DIR = os.path.dirname(__file__)
settings = appconfig(
    'config:' + os.path.join(TEST_DIR, 'test.ini'),
    name='static_map_generator'
)

with open(os.path.join(os.path.dirname(__file__), 'fixtures/grb_and_geojson.json'),
          'rb') as f:
    grb_and_geojson = json.loads(text_(f.read()))


class FunctionalTests(unittest.TestCase):
    def setUp(self):
        self.app = main({}, **settings)
        self.testapp = TestApp(self.app)

    def tearDown(self):
        del self.testapp, self.app
        testing.tearDown()


class RestFunctionalTests(FunctionalTests):

    @responses.activate
    def test_map_image(self):
        with open(os.path.join(os.path.dirname(__file__), 'fixtures/grb.png'), 'rb') as f:
            grb_image = f.read()
        responses.add(responses.GET,
                      'http://geoservices.informatievlaanderen.be/raadpleegdiensten/GRB-basiskaart-grijs/wms',
                      body=grb_image, status=200, content_type='application/json')
        res = self.testapp.post('/maps', json.dumps(grb_and_geojson),
                                headers={'Accept': 'application/octet-stream',
                                         'content-type': 'application/json'})
        self.assertIn('image/png', res.headers['Content-Type'])
        self.assertEqual('201 Created', res.status)

    @responses.activate
    def test_map_base64(self):
        with open(os.path.join(os.path.dirname(__file__), 'fixtures/grb.png'), 'rb') as f:
            grb_image = f.read()
        responses.add(responses.GET,
                      'http://geoservices.informatievlaanderen.be/raadpleegdiensten/GRB-basiskaart-grijs/wms',
                      body=grb_image, status=200, content_type='application/json')
        res = self.testapp.post('/maps', json.dumps(grb_and_geojson),
                                headers={'Accept': 'application/json',
                                         'content-type': 'application/json'})
        self.assertIn('application/json', res.headers['Content-Type'])
        self.assertEqual('201 Created', res.status)

    # def test_not_authorized(self):
    #     res = self.testapp.post('/maps', "{}",
    #                             headers={'Accept': 'application/json', 'Content-Type': 'application/json'},
    #                             expect_errors=True)
    #     self.assertEqual('401 Unauthorized', res.status)

    def test_not_found(self):
        res = self.testapp.post('/notfound', json.dumps({}),
                                headers={'Accept': 'application/json'},
                                expect_errors=True)
        self.assertEqual('404 Not Found', res.status)
        res = self.testapp.get('/maps', json.dumps({}),
                               headers={'Accept': 'application/json'}, expect_errors=True)
        self.assertEqual('404 Not Found', res.status)

    def test_failed_validation(self):
        res = self.testapp.post('/maps', json.dumps({}),
                                headers={'Accept': 'application/json'},
                                expect_errors=True)
        self.assertEqual(400, res.status_int)

    def test_validationerror(self):
        self.assertRaises(Exception, self.testapp.post, '/maps', "{}",
                          headers={'Accept': 'application/json'})
