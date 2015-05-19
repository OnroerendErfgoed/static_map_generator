from static_map_generator.generator import Generator

config_simple = {
    'params': {
        'filename': 'simple.png',
        'epsg': 4326,
        'filetype': 'png',
        'width': 500,
        'height': 500,
        'bbox': [4.95, 50.95, 5, 51]
    },
    'layers':
        [{'layer': {
            'type': 'text',
            'name': 'text.png',
            'text': 'This is a test',
            'font_size': 40,
            'text_color': '#FF3366'
        }

        },
            {'layer': {
                'type': 'wkt',
                'name': 'WKT',
                'wkt': 'POLYGON ((4.99 50.99, 4.995 50.99, 4.995 50, 4.99 50.99))',
                'color': 'steelblue',
                'opacity': 0.5
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
Generator.generate(config_simple)
