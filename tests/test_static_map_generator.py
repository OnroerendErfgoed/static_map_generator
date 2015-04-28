import unittest
from static_map_generator.static_map_generator import StaticMapGenerator


class MapMakerTests(unittest.TestCase):
    def test_static_map_generator(self):
        config_31370 = {
            'params': {
                'filename': 'tests/31370.png',
                'epsg': 31370,
                'filetype': 'png',
                'width': 500,
                'height': 500,
                'bbox': [145000, 195000, 165000, 215000]
            },
            'layers':
                [{'layer': {
                    'type': 'text',
                    'name': 'text.png',
                    'text': 'This is a test',
                    'color': '#FF3366',
                    'borderwidth': 1,
                    'font_size': 24,
                    'text_color': '#FF3366'
                }
                  },
                 {'layer': {
                     'type': 'logo',
                     'name': 'logo.png',
                     'path': 'resources/logo.png',
                     'opacity': 0.5
                 }
                  },
                 {'layer': {
                     'type': 'wkt',
                     'name': 'WKT',
                     'wkt': 'POLYGON ((155000 215000, 160000 210000, 160000 215000, 155000 215000))',
                     'color': 'steelblue',
                     'opacity': 0.5
                 }
                  },
                 {'layer': {
                     'type': 'wms',
                     'name': 'OE',
                     'url': 'https://geo.onroerenderfgoed.be/geoserver/wms?',
                     'layers': 'vioe_geoportaal:landschapsbeheersplannen',
                     'featureid': 'landschapsbeheersplannen.3816'
                 }
                  },
                 {'layer': {
                     'type': 'wms',
                     'name': 'ONBESTAAND',
                     'url': 'https://geo.onroerenderfgoed.be/geoserver/wms?',
                     'layers': 'vioe_geoportaal:onbestaande_laag'
                 }
                  },
                 {'layer': {
                     'type': 'wms',
                     'name': 'GRB',
                     'url': 'http://geo.api.agiv.be/geodiensten/raadpleegdiensten/GRB-basiskaart/wmsgr?',
                     'layers': 'GRB_BSK'
                 }
                  }
                 ]
        }

        StaticMapGenerator.generate(config_31370)


        config_4326 = {
            'params': {
                'filename': 'tests/4326.png',
                'epsg': 4326,
                'filetype': 'png',
                'width': 500,
                'height': 500,
                'bbox': [4, 50, 5, 51]
            },
            'layers':
                [{'layer': {
                    'type': 'text',
                    'name': 'text.png',
                    'text': 'This is a test',
                    'color': '#FF3366',
                    'borderwidth': 1,
                    'font_size': 24,
                    'text_color': '#FF3366'
                }
                  },
                 {'layer': {
                     'type': 'logo',
                     'name': 'logo.png',
                     'path': 'resources/logo.png',
                     'opacity': 0.5
                 }
                  },
                 {'layer': {
                     'type': 'wkt',
                     'name': 'WKT',
                     'wkt': 'POLYGON ((4.5 50.2, 5 50.2, 5 50, 4.5 50.2))',
                     'color': 'steelblue',
                     'opacity': 0.5
                 }
                  },
                 {'layer': {
                     'type': 'wms',
                     'name': 'OE',
                     'url': 'https://geo.onroerenderfgoed.be/geoserver/wms?',
                     'layers': 'vioe_geoportaal:landschapsbeheersplannen',
                     'featureid': 'landschapsbeheersplannen.3816'
                 }
                  },
                 {'layer': {
                     'type': 'wms',
                     'name': 'GRB',
                     'url': 'http://geo.api.agiv.be/geodiensten/raadpleegdiensten/GRB-basiskaart/wmsgr?',
                     'layers': 'GRB_BSK'
                 }
                  }
                 ]
        }
        StaticMapGenerator.generate(config_4326)