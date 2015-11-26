from static_map_generator.generator import Generator

config_4326 = {
    'params': {
        'filename': '4326.png',
        'epsg': 4326,
        'filetype': 'png',
        'width': 500,
        'height': 500,
        'bbox': [4, 50, 5, 51]
    },
    'layers':
        [{
            'type': 'text',
            'text': 'This is a test',
            'font_size': 24,
            'text_color': '#FF3366'

          },
         {
             'type': 'logo',
             'url': 'https://www.onroerenderfgoed.be/assets/img/logo-og.png',
             'opacity': 0.5

          },
         {
             'type': 'wkt',
             'wkt': 'POLYGON ((4.5 50.2, 5 50.2, 5 50, 4.5 50.2))',
             'color': 'steelblue',
             'opacity': 0.5

          },
         {
             'type': 'wms',
             'url': 'https://geo.onroerenderfgoed.be/geoserver/wms?',
             'layers': 'vioe_geoportaal:landschapsbeheersplannen',
             'featureid': 'landschapsbeheersplannen.3816'

          },
         {
             'type': 'wms',
             'url': 'http://geo.api.agiv.be/geodiensten/raadpleegdiensten/GRB-basiskaart/wmsgr?',
             'layers': 'GRB_BSK'

          }
         ]
}
Generator.generate(config_4326)