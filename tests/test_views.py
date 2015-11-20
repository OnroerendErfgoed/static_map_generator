import unittest

from pyramid import testing
from geozoekdiensten.validators import ValidationError
from pyramid.httpexceptions import HTTPBadRequest

try:
    from unittest.mock import Mock, patch
except:
    from mock import Mock, patch


def _registerRoutes(config):
    config.add_route('afbakeningen', '/afbakeningen')
    config.add_route('administratievegrenzen', '/administratievegrenzen')
    config.add_route('home', '/')
    settings = {
        'admingrenzen.url': 'https://www.mercator.vonet.be/raadpleegdienstenmercatorintern/au/ows',
        'admingrenzen.geometry_field': 'the_geom',
        'admingrenzen.gemeente': 'au:au_gemt_vlaa',
        'admingrenzen.provincie': 'au:au_prov_vlaa',
        'admingrenzen.arrondissement': 'au:au_arron_vlaa',
        'admingrenzen.gewest': 'au:au_gew_vlaa',
        'admingrenzen.name_field': 'naam',
        'admingrenzen.niscode_field': 'niscode'
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
    def _get_params_data(self):
        return {"categorie": "objecten",
                "buffer": "2",
                "geometrie": {
                    "type": "Polygon",
                    "coordinates": [[[209289.18, 173495.99], [209289.18, 186116.7], [223498.88, 186116.7],
                                     [223498.88, 173495.99], [209289.18, 173495.99]]]}
                }

    def _get_params_data2(self):
        return {
            "categorie": "objecten",
            "buffer": "2",
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

    def _get_rest_view(self, request):
        from geozoekdiensten.views.views import RestView

        return RestView(request)

    def _get_afbakening_view(self, request):
        from geozoekdiensten.views.views import AfbakeningenView

        return AfbakeningenView(request)

    def test_home(self):
        from geozoekdiensten.views.views import AfbakeningenView

        afbakeningenview = AfbakeningenView(self.request)
        home = afbakeningenview.home()
        self.assertEqual('200 OK', home.status)

    @patch('geozoekdiensten.views.views.get_system_token', Mock(return_value="test_token"))
    def test_handle_invalid(self):
        from geozoekdiensten.views.views import AdmingrenzenView

        self.request.params = {"type": "gemeente"}
        admingrenzenview = AdmingrenzenView(self.request)
        self.assertRaises(ValidationError, admingrenzenview.administratievegrenzen_by_get)

    def test_handle_invalid2(self):
        from geozoekdiensten.views.views import AfbakeningenView

        self.request.params = {"categorie": "objecten"}
        afbakeningenview = AfbakeningenView(self.request)
        self.assertRaises(ValidationError, afbakeningenview.afbakeningen_by_get)

    def test_set_response_header(self):
        rv = self._get_rest_view(self.request)
        rv.set_response_header(100, 3)
        self.assertEqual('items 0-2/100', self.request.response.headers['Content-Range'])

    def test_get_request_header(self):
        self.request.headers['Range'] = 'items=0-2'
        rv = self._get_rest_view(self.request)
        results = rv.parse_range_header([1, 2, 3, 4])
        self.assertEqual([1, 2], results)

    def test_parse_range_header(self):
        rv = self._get_rest_view(self.request)
        results = rv.parse_range_header([1, 2, 3, 4])
        self.assertEqual([1, 2, 3, 4], results)

    def test_parse_range_header_2(self):
        self.request.headers['Range'] = 'items='
        rv = self._get_rest_view(self.request)
        results = rv.parse_range_header([1, 2, 3, 4])
        self.assertEqual([1, 2, 3, 4], results)

    def check_test_search_params(self, search_params):
        self.assertIn('categorie', search_params)
        self.assertEqual('objecten', search_params['categorie'])
        self.assertIn('buffer', search_params)
        self.assertEqual('2', search_params['buffer'])
        self.assertIn('geometrie', search_params)
        self.assertIn('type', search_params['geometrie'])
        self.assertEqual("Polygon", search_params['geometrie']['type'])
        self.assertIn('coordinates', search_params['geometrie'])
        self.assertEqual([[[209289.18, 173495.99], [209289.18, 186116.7], [223498.88, 186116.7],
                           [223498.88, 173495.99], [209289.18, 173495.99]]], search_params['geometrie']['coordinates'])

    def test_get_params_get(self):
        rv = self._get_rest_view(self.request)
        data = self._get_params_data()
        self.request.params = data
        valid_params = ['categorie', 'geometrie', 'buffer', 'geef_geometrie']
        search_params = rv._get_valid_params(self.request.params, valid_params)
        self.check_test_search_params(search_params)

    def test_get_params_post(self):
        rv = self._get_rest_view(self.request)
        data = self._get_params_data()
        self.request.json_body = data
        params = rv._get_params()
        valid_params = ['categorie', 'geometrie', 'buffer', 'geef_geometrie']
        search_params = rv._get_valid_params(params, valid_params)
        self.check_test_search_params(search_params)

    def test_get_params_post_leeg(self):
        rv = self._get_rest_view(self.request)
        self.assertRaises(HTTPBadRequest, rv._get_params)
