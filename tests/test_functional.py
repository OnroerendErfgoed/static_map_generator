import os, unittest, json

import pytest

from paste.deploy.loadwsgi import appconfig

from pyramid import testing
from webtest import TestApp

from geozoekdiensten import main

TEST_DIR = os.path.dirname(__file__)
settings = appconfig(
    'config:' + os.path.join(TEST_DIR, 'test.ini'),
    name='geozoekdiensten'
)


@pytest.mark.skipif(os.getenv('TRAVIS', False) != False, reason='No integration tests on Travis-ci.')
class FunctionalTests(unittest.TestCase):
    def setUp(self):
        self.app = main({}, **settings)
        self.testapp = TestApp(self.app)

    def tearDown(self):
        del self.testapp, self.app
        testing.tearDown()


class RestFunctionalTests(FunctionalTests):
    def _get_params_point_buffer(self):
        return {"categorie": "objecten",
                "buffer": "1000",
                "geometrie": {
                    "type": "Point",
                    "coordinates": [209289.18, 173495.99],
                    "crs": {
                        "type": "name",
                        "properties": {
                            "name": "urn:ogc:def:crs:EPSG::31370"
                        }
                    }
                }
                }

    def _get_params_point(self):
        return {"geometrie": {
            "type": "Point",
            "coordinates": [209289.18, 173495.99],
            "crs": {
                "type": "name",
                "properties": {
                    "name": "urn:ogc:def:crs:EPSG::31370"
                }
            }
        }
        }

    def _get_params_intersecting_multipolygon(self):
        return {"categorie": "objecten",
                "geometrie": {
                    "type": "MultiPolygon",
                    "coordinates": [[[[103827.44321801752, 192484.5100535322], [103826.65621839411, 192565.57026445214],
                                      [103839.2000972359, 192622.4958831761], [103877.27257229008, 192673.1911981115],
                                      [103981.90807816133, 192592.71585010737],
                                      [104050.62835409257, 192535.07265175506],
                                      [104119.78606355426, 192526.95860514138], [104157.5529127745, 192543.1371434061],
                                      [104163.33481632298, 192516.068607972], [104043.86794770884, 192451.07658289373],
                                      [103839.39232099024, 192304.2814310426], [103825.49962980268, 192434.99411542248],
                                      [103827.44321801752, 192484.5100535322]]]],
                    "crs": {
                        "type": "name",
                        "properties": {
                            "name": "urn:ogc:def:crs:EPSG::31370"}}}
                }

    def _get_params_multipolygon(self):
        return {"categorie": "objecten",
                "geometrie": {
                    "type": "MultiPolygon",
                    "coordinates": [[[[103827.44321801752, 192484.5100535322], [103826.65621839411, 192565.57026445214],
                                      [103839.2000972359, 192622.4958831761], [103877.27257229008, 192673.1911981115],
                                      [103981.90807816133, 192592.71585010737],
                                      [104050.62835409257, 192535.07265175506],
                                      [104119.78606355426, 192526.95860514138], [104157.5529127745, 192543.1371434061],
                                      [104163.33481632298, 192516.068607972], [104043.86794770884, 192451.07658289373],
                                      [103839.39232099024, 192304.2814310426], [103825.49962980268, 192434.99411542248],
                                      [103827.44321801752, 192484.5100535322]]]],
                    "crs": {
                        "type": "name",
                        "properties": {
                            "name": "urn:ogc:def:crs:EPSG::31370"}}}
                }

    def _get_params_buffer(self):
        return {"categorie": "objecten",
                "buffer": "2000",
                "geometrie": {
                    "type": "Point",
                    "coordinates": [209289.18, 173495.99],
                    "crs": {
                        "type": "name",
                        "properties": {
                            "name": "urn:ogc:def:crs:EPSG::31370"
                        }
                    }
                }
                }

    def _get_params_polygon(self):
        return {
            "geometrie": {"type": "Polygon",
                          "coordinates": [[[3.17, 51.23], [3.96, 51], [4.003, 51.01], [3.17, 51.23]]],
                          "crs": {
                              "type": "name",
                              "properties": {
                                  "name": "EPSG:4326"}
                          }
                          }
        }

    def _get_params_point_buffer_dossiers(self):
        return {"categorie": "dossiers",
                "buffer": "1000",
                "geometrie": {
                    "type": "Point",
                    "coordinates": [156934.202067326, 193249.128686974],
                    "crs": {
                        "type": "name",
                        "properties": {
                            "name": "urn:ogc:def:crs:EPSG::31370"
                        }
                    }
                }
                }

    def test_search_point_buffer(self):
        self.testapp.get('/mock_user')
        res = self.testapp.post('/afbakeningen', json.dumps(self._get_params_point_buffer()),
                                headers={'Accept': 'application/json', 'Range': 'items=0-10000'})
        self.assertIn('application/json', res.headers['Content-Type'])
        self.assertIn('Content-Range', res.headers)
        self.assertEqual('200 OK', res.status)
        data = json.loads(res.body.decode('utf-8'))
        for data_elem in data:
            print("response data: " + str(data_elem))
        self.assertIsInstance(data, list)

    def test_search_polygon(self):
        self.testapp.get('/mock_user')
        res = self.testapp.post('/afbakeningen', json.dumps(self._get_params_polygon()),
                                headers={'Accept': 'application/json', 'Range': 'items=0-10000'})
        self.assertIn('application/json', res.headers['Content-Type'])
        self.assertIn('Content-Range', res.headers)
        self.assertEqual('200 OK', res.status)
        data = json.loads(res.body.decode('utf-8'))
        for data_elem in data:
            print("response data: " + str(data_elem))
        self.assertIsInstance(data, list)

    def test_search_multipolygon(self):
        self.testapp.get('/mock_user')
        res = self.testapp.post('/afbakeningen', json.dumps(self._get_params_multipolygon()),
                                headers={'Accept': 'application/json', 'Range': 'items=0-10000'})
        self.assertIn('application/json', res.headers['Content-Type'])
        self.assertIn('Content-Range', res.headers)
        self.assertEqual('200 OK', res.status)
        data = json.loads(res.body.decode('utf-8'))
        for data_elem in data:
            print("response data: " + str(data_elem))
        self.assertIsInstance(data, list)

    def test_search_intersecting_multipolygon(self):
        self.testapp.get('/mock_user')
        res = self.testapp.post('/afbakeningen', json.dumps(self._get_params_intersecting_multipolygon()),
                                headers={'Accept': 'application/json', 'Range': 'items=0-10000'})
        self.assertIn('application/json', res.headers['Content-Type'])
        self.assertIn('Content-Range', res.headers)
        self.assertEqual('200 OK', res.status)
        data = json.loads(res.body.decode('utf-8'))
        for data_elem in data:
            print("response data: " + str(data_elem))
        self.assertIsInstance(data, list)

    def test_search_buffer(self):
        self.testapp.get('/mock_user')
        res = self.testapp.post('/afbakeningen', json.dumps(self._get_params_buffer()),
                                headers={'Accept': 'application/json', 'Range': 'items=0-10000'})
        self.assertIn('application/json', res.headers['Content-Type'])
        self.assertIn('Content-Range', res.headers)
        self.assertEqual('200 OK', res.status)
        data = json.loads(res.body.decode('utf-8'))
        for data_elem in data:
            print("response data: " + str(data_elem))
        self.assertIsInstance(data, list)

    def test_search_point(self):
        self.testapp.get('/mock_user')
        res = self.testapp.post('/afbakeningen', json.dumps(self._get_params_point()),
                                headers={'Accept': 'application/json', 'Range': 'items=0-10000'})
        self.assertIn('application/json', res.headers['Content-Type'])
        self.assertIn('Content-Range', res.headers)
        self.assertEqual('200 OK', res.status)
        data = json.loads(res.body.decode('utf-8'))
        for data_elem in data:
            print("response data: " + str(data_elem))
        self.assertIsInstance(data, list)

    def test_search_point_dossiers(self):
        self.testapp.get('/mock_user')
        res = self.testapp.post('/afbakeningen', json.dumps(self._get_params_point_buffer_dossiers()),
                                headers={'Accept': 'application/json', 'Range': 'items=0-10000'})
        self.assertIn('application/json', res.headers['Content-Type'])
        self.assertIn('Content-Range', res.headers)
        self.assertEqual('200 OK', res.status)
        data = json.loads(res.body.decode('utf-8'))
        for data_elem in data:
            print("response data: " + str(data_elem))
        self.assertIsInstance(data, list)

    def test_search_admingrenzen_point(self):
        self.testapp.get('/mock_user')
        params = self._get_params_point()
        params['type'] = 'gemeente'
        res = self.testapp.post('/administratievegrenzen', json.dumps(params), headers={'Accept': 'application/json'})
        self.assertIn('application/json', res.headers['Content-Type'])
        self.assertIn('Content-Range', res.headers)
        self.assertEqual('200 OK', res.status)
        data = json.loads(res.body.decode('utf-8'))
        for data_elem in data:
            print("response data: " + str(data_elem))
            self.assertIn('id', data_elem)
            self.assertIn('naam', data_elem)
            self.assertIn('type', data_elem)
            self.assertIn('geometrie', data_elem)
            self.assertIn('type', data_elem['geometrie'])
            self.assertIn('coordinates', data_elem['geometrie'])
            self.assertIn('crs', data_elem['geometrie'])
        self.assertIsInstance(data, list)

    def test_search_admingrenzen_point_buffer(self):
        self.testapp.get('/mock_user')
        params = self._get_params_point_buffer()
        params['type'] = ['gemeente', 'gewest']
        res = self.testapp.post('/administratievegrenzen', json.dumps(params), headers={'Accept': 'application/json'})
        self.assertEqual('200 OK', res.status)

    def test_search_admingrenzen_polygon(self):
        self.testapp.get('/mock_user')
        params = self._get_params_polygon()
        params['type'] = "provincie;arrondissement"
        res = self.testapp.post('/administratievegrenzen', json.dumps(params), headers={'Accept': 'application/json'})
        self.assertEqual('200 OK', res.status)

    def test_admingrenzen_get(self):
        res = self.testapp.get(
            '/administratievegrenzen?type=gemeente&type=gewest&geometrie={"type":"Point","coordinates":[4.430750, 51.149166]}&buffer=1000',
            headers={'Accept': 'application/json'})
        self.assertEqual('200 OK', res.status)

    def test_afbakeningen_get(self):
        res = self.testapp.get(
            '/afbakeningen?geometrie={"type":"Point","coordinates":[4.430750, 51.149166]}&buffer=1000',
            headers={'Accept': 'application/json'})
        self.assertEqual('200 OK', res.status)

    def test_afbakeningen_geef_geometrie(self):
        res = self.testapp.get(
            '/afbakeningen?categorie=objecten&geef_geometrie=0&geometrie={"type":"Point","coordinates":[4.430750, 51.149166]}&buffer=1000',
            headers={'Accept': 'application/json'})
        data = json.loads(res.body.decode('utf-8'))
        for data_elem in data:
            print("response data: " + str(data_elem))
            self.assertIn('id', data_elem)
            self.assertIn('naam', data_elem)
            self.assertIn('type', data_elem)
            self.assertNotIn('geometrie', data_elem)
        self.assertIsInstance(data, list)

    def test_administratievegrenzen_geef_geometrie(self):
        res = self.testapp.get(
            '/administratievegrenzen?geef_geometrie=0&geometrie={"type":"Point","coordinates":[4.430750, 51.149166]}&buffer=1000',
            headers={'Accept': 'application/json'})
        data = json.loads(res.body.decode('utf-8'))
        for data_elem in data:
            print("response data: " + str(data_elem))
            self.assertIn('id', data_elem)
            self.assertIn('naam', data_elem)
            self.assertIn('type', data_elem)
            self.assertNotIn('geometrie', data_elem)
        self.assertIsInstance(data, list)
