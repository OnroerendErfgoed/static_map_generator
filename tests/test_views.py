import unittest
import os
import json

from paste.deploy.loadwsgi import appconfig
from pyramid.testing import DummyRequest
from pyramid.httpexceptions import HTTPBadRequest
from pyramid.compat import text_

try:
    from unittest.mock import Mock, patch, MagicMock, PropertyMock
except:
    from mock import Mock, patch, MagicMock, PropertyMock

from static_map_generator.views.views import RestView
from static_map_generator.validators import ValidationFailure
from static_map_generator.views.exceptions import internal_server_error
import responses


settings = appconfig('config:' + os.path.join(os.path.dirname(__file__), 'test.ini'))
with open(os.path.join(os.path.dirname(__file__), 'fixtures/grb_and_geojson.json'), 'rb') as f:
    grb_and_geojson = json.loads(text_(f.read()))


class ViewTests(unittest.TestCase):
    def setUp(self):
        self.request = DummyRequest()
        self.request.registry.settings = settings

    def tearDown(self):
        pass

    def test_get_params(self):
        self.assertRaises(HTTPBadRequest, RestView(self.request)._get_params)

        self.request.json_body = {}
        params = RestView(self.request)._get_params()
        self.assertDictEqual({}, params)

        self.request = MagicMock()
        p = PropertyMock(side_effect=ValueError)
        type(self.request).json_body = p
        self.assertRaises(HTTPBadRequest, RestView(self.request)._get_params)

    def test_validate_config(self):
        self.request.json_body = {}
        rest_view = RestView(self.request)
        params = rest_view._get_params()
        self.assertRaises(ValidationFailure, rest_view.validate_config, params)

    def test_home(self):
        rest_view = RestView(self.request)
        home = rest_view.home()
        self.assertEqual('200 OK', home.status)

    @responses.activate
    def test_maps_by_post(self):
        with open(os.path.join(os.path.dirname(__file__), 'fixtures/grb.png'), 'rb') as f:
            grb_image = f.read()
        responses.add(responses.GET,
                      'http://geoservices.informatievlaanderen.be/raadpleegdiensten/GRB-basiskaart-grijs/wms',
                      body=grb_image, status=200, content_type='application/json')
        self.request.json_body = grb_and_geojson
        rest_view = RestView(self.request)
        res = rest_view.maps_by_post_stream()
        self.assertEqual('200 OK', res.status)
        self.assertIsNotNone(res.body)

    @responses.activate
    def test_maps_by_post_base64(self):
        with open(os.path.join(os.path.dirname(__file__), 'fixtures/grb.png'), 'rb') as f:
            grb_image = f.read()
        responses.add(responses.GET,
                      'http://geoservices.informatievlaanderen.be/raadpleegdiensten/GRB-basiskaart-grijs/wms',
                      body=grb_image, status=200, content_type='application/json')
        self.request.json_body = grb_and_geojson
        rest_view = RestView(self.request)
        res = rest_view.maps_by_post_base64()
        self.assertIsNotNone(res['image'])

    def test_internal_error(self):
        res = internal_server_error(Exception(), self.request)
        expected_msg = 'Er ging iets fout in de server. Onze excuses. Stel je fouten vast of heb je een vraag? ' \
                       'Mail dan naar ict@onroerenderfgoed.be'
        self.assertDictEqual({'detail': '', 'message': expected_msg}, res)
