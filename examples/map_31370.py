from static_map_generator.generator import Generator


config_31370 = {
    'params': {
        'filename': '31370.png',
        'epsg': 31370,
        'filetype': 'png',
        'width': 500,
        'height': 500,
        'bbox': [145000, 195000, 165000, 215000]
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
             'wkt': 'POLYGON ((155000 215000, 160000 210000, 160000 215000, 155000 215000))',
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
             'url': 'https://geo.onroerenderfgoed.be/geoserver/wms?',
             'layers': 'vioe_geoportaal:onbestaande_laag'

          },
         {
             'type': 'wms',
             'url': 'http://geo.api.agiv.be/geodiensten/raadpleegdiensten/GRB-basiskaart/wmsgr?',
             'layers': 'GRB_BSK'

          }
         ]
}

Generator.generate(config_31370)
