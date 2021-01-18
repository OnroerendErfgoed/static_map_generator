import os

from static_map_generator.generator import Generator

examples = [
    {
        "name": "map_simple_example_1.png",
        "coordinates": [
            [
                [173226.56, 174184.28],
                [173300.48, 174325.52],
                [173323.41, 174314.54],
                [173259.49, 174172.57],
                [173226.56, 174184.28]
            ]
        ]
    }, {
        "name": "map_simple_example_2.png",
        "coordinates": [
            [
                [169839.02, 178535.12],
                [168247.34, 166934.73],
                [185701.87, 170037.16],
                [185701.87, 170118.09],
                [169839.02, 178535.12]
            ]
        ]
    }
]

for example in examples:
    config_simple = {
        "params": {
            "width": 325,
            "height": 500
        },
        "layers": [
            {
                "geojson": {
                    "coordinates": example["coordinates"],
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

    with open(os.path.join(os.path.dirname(__file__), example["name"]), 'wb') as f:
        f.write(Generator.generate_stream(config_simple))
