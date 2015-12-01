import unittest
from static_map_generator.validators import uri_validator, wkt_validator, geojson_validator, string_validator, \
    number_validator, scale_validator, gravity_validator, required_validator, optional_validator, ConfigSchemaNode
from colander import Invalid

config = {
    "params": {
        "filename": "31370.png",
        "epsg": 31370,
        "filetype": "png",
        "width": 500,
        "height": 500,
        "bbox": [145000.0, 195000.0, 165000.0, 215000.0]
    },
    "layers":
        [{
            "type": "text",
            "text": "This is a test",
            "font_size": 24,
            "text_color": "#FF3366",
            "gravity": "north_west"
        },
            {
                "type": "logo",
                "url": "https://www.onroerenderfgoed.be/assets/img/logo-og.png",
                "opacity": 0.5,
                "imagewidth": 100,
                "imageheight": 100,
                "offset": "0,0",
                "gravity": "south_east"

            },
            {
                "type": "wkt",
                "wkt": "POLYGON ((155000 215000, 160000 210000, 160000 215000, 155000 215000))",
                "color": "steelblue",
                "opacity": 0.5

            },
                        {
                "type": "wkt",
            'wkt': 'MULTIPOINT ((103500 192390.11), (103912.03 192390.11))',
                "color": "steelblue",
                "opacity": 0.5

            },
                        {
                "type": "wkt",
            'wkt': 'MULTIPOINT (103500 192390.11, 103912.03 192390.11)',
                "color": "steelblue",
                "opacity": 0.5

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
                'geojson':{'crs': {'type': 'name', 'properties': {'name': 'EPSG:31370'}}, 'type': 'MultiPoint', 'coordinates': [[103912.03, 192390.11],[103500, 192390.11]]},
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

    def test_wkt_validator(self):
        wkt_validator(test_node, 'POINT (30 10)')
        self.assertRaises(Invalid, wkt_validator, test_node, 'test')

    def test_geojson_validator(self):
        geojson_validator(test_node, {'crs': {'type': 'name', 'properties': {'name': 'EPSG:31370'}}, 'type': 'MultiPoint', 'coordinates': [[103912.03, 192390.11],[103500, 192390.11]]})
        self.assertRaises(Invalid, geojson_validator, test_node, 'test')

    def test_string_validator(self):
        string_validator(test_node, 'string')
        self.assertRaises(Invalid, string_validator, test_node, 2452)

    def test_number_validator(self):
        number_validator(test_node, 2152)
        self.assertRaises(Invalid, number_validator, test_node, 'test')

    def test_scale_validator(self):
        scale_validator(test_node, 0.6)
        self.assertRaises(Invalid, scale_validator, test_node, 1.2)

    def test_gravity_validator(self):
        gravity_validator(test_node, 'center')
        self.assertRaises(Invalid, gravity_validator, test_node, 'north')

    def test_optional_validator(self):
        optional_validator('test', 'value', test_node, {}, string_validator)
        self.assertRaises(Invalid, optional_validator, 'test', 'value', test_node, {'test': 'value'}, number_validator)

    def test_required_validator(self):
        required_validator('test', 'text', test_node, {'test': 'value'}, string_validator)
        self.assertRaises(Invalid, required_validator, 'test', 'text', test_node, {'invalid': 'value'}, string_validator)
