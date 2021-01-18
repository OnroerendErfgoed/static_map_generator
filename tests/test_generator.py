import os
import unittest
from copy import deepcopy

import responses

from static_map_generator.generator import Generator

try:
    from unittest.mock import patch, call
except:
    from unittest.mock import patch, call

config = {
    "params": {
        "width": 325,
        "height": 500
    },
    "layers": [
        {
            "geojson": {
                "coordinates": [
                    [
                        [173226.56, 174184.28],
                        [173300.48, 174325.52],
                        [173323.41, 174314.54],
                        [173259.49, 174172.57],
                        [173226.56, 174184.28]
                    ]
                ],
                "type": "Polygon"
            },
            "type": "geojson"
        },
        {
            "type": "text",
            "text": "© GRB basiskaart, informatie Vlaanderen",
            "gravity": "south_east",
            "font_size": 3
        },
        {

            "type": "wms",
            "url": "http://geoservices.informatievlaanderen.be/raadpleegdiensten/GRB-basiskaart-grijs/wms?",
            "layers": "GRB_BSK_GRIJS"
        }
    ]
}

with open(os.path.join(os.path.dirname(__file__), 'fixtures/grb.png'), 'rb') as f:
    grb_image = f.read()


def _init_responses():
    responses.add(responses.GET,
                  'http://geoservices.informatievlaanderen.be/raadpleegdiensten/GRB-basiskaart-grijs/wms',
                  body=grb_image, status=200, content_type='application/json')


class UtilsTests(unittest.TestCase):

    @responses.activate
    def test_stream(self):
        _init_responses()
        Generator.generate_stream(config)

    @responses.activate
    def test_stream_wms_error(self):
        responses.add(responses.GET,
                      'http://geoservices.informatievlaanderen.be/raadpleegdiensten/GRB-basiskaart-grijs/wms',
                      status=500)
        with patch('static_map_generator.generator.log') as log_mock:
            with self.assertRaises(Exception):
                Generator.generate_stream(config)
        self.assertEqual(log_mock.error.call_count, 2)
        self.assertIn(call('Background wms could not be rendered'),
                      log_mock.error.mock_calls)

    @responses.activate
    def test_stream_geojson_error(self):
        _init_responses()
        config_json_error = deepcopy(config)
        del config_json_error['layers'][0]['geojson']
        with patch('static_map_generator.generator.log') as log_mock:
            with self.assertRaises(Exception):
                Generator.generate_stream(config_json_error)
        self.assertEqual(log_mock.error.call_count, 2)
        self.assertIn(call('Following layer could not be rendered: 0'),
                      log_mock.error.mock_calls)

    @responses.activate
    def test_stream_text_error(self):
        _init_responses()
        config_text_error = deepcopy(config)
        del config_text_error['layers'][1]['text']
        with patch('static_map_generator.generator.log') as log_mock:
            with self.assertRaises(Exception):
                Generator.generate_stream(config_text_error)
        self.assertEqual(log_mock.error.call_count, 2)
        self.assertIn(call('Text could not be rendered'), log_mock.error.mock_calls)
