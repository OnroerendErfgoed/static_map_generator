from static_map_generator.generator import Generator

config_simple = {
    'params': {
        'filename': 'simple.png',
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
            'font_size': 24,
            'text_color': '#FF3366'
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
                'name': 'GRB',
                'url': 'http://geo.api.agiv.be/geodiensten/raadpleegdiensten/GRB-basiskaart/wmsgr?',
                'layers': 'GRB_BSK'
            }
            }
        ]
}
Generator.generate(config_simple)
