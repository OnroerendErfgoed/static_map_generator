import unittest

from colander import Invalid

from static_map_generator.validators import ConfigSchemaNode
from static_map_generator.validators import ValidationFailure
from static_map_generator.validators import geojson_validator
from static_map_generator.validators import gravity_validator
from static_map_generator.validators import number_validator
from static_map_generator.validators import optional_validator
from static_map_generator.validators import required_validator
from static_map_generator.validators import string_validator
from static_map_generator.validators import uri_validator

config = {
    "params": {
        "filename": "31370.png",
        "width": 500,
        "height": 500,
        "bbox": [145000.0, 195000.0, 165000.0, 215000.0]
    },
    "layers":
        [
            {
                "type": "text",
                "text": "This is a test",
                "font_size": 24,
                "gravity": "north_west"
            },
            {
                "type": "wms",
                "url": "https://geo.onroerenderfgoed.be/geoserver/wms?",
                "layers": "vioe_geoportaal:landschapsbeheersplannen",
                "featureid": "landschapsbeheersplannen.3816"

            },
            {
                "type": "wms",
                "url": "http://geo.api.agiv.be/geodiensten/raadpleegdiensten/GRB-basiskaart/wmsgr?",
                "layers": "GRB_BSK"

            },
            {
                'color': 'steelblue',
                'opacity': 0.5,
                'type': 'geojson',
                'geojson': {'crs': {'type': 'name', 'properties': {'name': 'EPSG:31370'}},
                            'type': 'MultiPoint',
                            'coordinates': [[103912.03, 192390.11], [103500, 192390.11]]},
            }
        ]
}


class Node:
    def __init__(self, name):
        self.name = name


test_node = Node('test_node')


class ValidateParamsTests(unittest.TestCase):
    def setUp(self):
        pass

    def test_validation_failure(self):
        a = ValidationFailure('msg', 'errors')
        self.assertEqual('msg', a.msg)
        self.assertEqual('errors', a.errors)

    def test_config(self):
        config_schema = ConfigSchemaNode()
        config_res = config_schema.deserialize(config)
        self.maxDiff = None
        self.assertDictEqual(config['params'], config_res['params'])
        for index in range(0, len(config['layers'])):
            self.assertDictEqual(config['layers'][index], config_res['layers'][index])

    def test_uri_validator(self):
        uri_validator(test_node, 'http://www.test.com')
        self.assertRaises(Invalid, uri_validator, test_node, 'test')

    def test_geojson_validator(self):
        geojson_validator(test_node,
                          {'crs': {'type': 'name', 'properties': {'name': 'EPSG:31370'}},
                           'type': 'MultiPoint',
                           'coordinates': [[103912.03, 192390.11], [103500, 192390.11]]})
        self.assertRaises(Invalid, geojson_validator, test_node, 'test')

    def test_number_validator(self):
        number_validator(test_node, 2152)
        self.assertRaises(Invalid, number_validator, test_node, 'test')

    def test_gravity_validator(self):
        gravity_validator(test_node, 'center')
        self.assertRaises(Invalid, gravity_validator, test_node, 'north')

    def test_optional_validator(self):
        optional_validator('test', 'value', test_node, {}, string_validator)
        self.assertRaises(Invalid, optional_validator, 'test', 'value', test_node,
                          {'test': 'value'}, number_validator)

    def test_required_validator(self):
        required_validator('test', 'text', test_node, {'test': 'value'}, string_validator)
        self.assertRaises(Invalid, required_validator, 'test', 'text', test_node,
                          {'invalid': 'value'}, string_validator)
