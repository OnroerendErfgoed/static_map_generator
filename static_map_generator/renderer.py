# -*- coding: utf-8 -*-
"""
Adapters to help render map layers
"""
from abc import ABCMeta, abstractmethod
import json
from pyramid.renderers import JSON
import requests
import mapnik
from wand.color import Color
from wand.image import Image
from static_map_generator.utils import merge_dicts, calculate_scale
from wand.drawing import Drawing

json_item_renderer = JSON()


class Renderer(object):
    __metaclass__ = ABCMeta

    @staticmethod
    def factory(layer_type):
        if layer_type == "wms":
            return WmsRenderer()
        elif layer_type == "geojson":
            return GeojsonRenderer()
        elif layer_type == "text":
            return TextRenderer()
        elif layer_type == "scale":
            return ScaleRenderer()
        else:
            return DefaultRenderer()

    @abstractmethod
    def render(self, **kwargs):     # pragma: no cover
        pass

    @abstractmethod
    def type(self):                 # pragma: no cover
        pass


class WmsRenderer(Renderer):
    def render(self, **kwargs):
        params = {
            "layers": kwargs['layers'],
            "transparent": "TRUE",
            "format": "image/png",
            "service": "WMS",
            "version": "1.1.0",
            "request": "GetMap",
            "styles": '',
            "srs": "EPSG:31370",
            "bbox": str(kwargs['bbox'][0]) + "," + str(kwargs['bbox'][1]) + "," + str(kwargs['bbox'][2]) + ","
                    + str(kwargs['bbox'][3]),
            "width": kwargs['width'],
            "height": kwargs['height']
        }
        params = merge_dicts(kwargs, params)
        res = requests.get(kwargs['url'], params=params)
        res.raise_for_status()
        return res.content

    def type(self):
        return "wms"


class GeojsonRenderer(Renderer):
    def render(self, **kwargs):
        # fix to create valid geojson from contour
        geojson = {"type": "Feature", "properties": {}, "geometry": {}, 'geometry': kwargs['geojson']}
        ds = mapnik.MemoryDatasource()
        feature = mapnik.Feature.from_geojson(json.dumps(geojson), mapnik.Context())
        ds.add_feature(feature)
        layer = mapnik.Layer('geojson' + str(kwargs['idx']), '+init=epsg:31370')
        layer.datasource = ds
        return layer

    def type(self):
        return "geojson"


class TextRenderer(Renderer):
    def render(self, **kwargs):

        with Image(filename=kwargs['filename'], resolution=300) as image:
            with Drawing() as draw:
                draw.font = '/Library/Fonts/Verdana.ttf'
                draw.font_size = kwargs['font_size']
                draw.fill_color = Color('black')
                draw.text_under_color = (Color('white'))
                draw.gravity = kwargs['gravity']
                draw.text(0, 0, kwargs['text'])
                draw(image)

            image.save(filename=kwargs['filename'])

    def type(self):
        return "text"


class ScaleRenderer(Renderer):
    def render(self, **kwargs):
        scale_width, scale_label = calculate_scale(kwargs['map_scale'], kwargs['width'])
        buffer = 5

        with Image(filename=kwargs['filename'], resolution=300) as image:
            with Drawing() as draw:
                draw.stroke_color = Color('white')
                draw.fill_color = Color('white')
                points = [(0, kwargs['height'] - buffer * 4),
                          (0, kwargs['height']),
                          (scale_width + (buffer * 2), kwargs['height']),
                          (scale_width + (buffer * 2), kwargs['height'] - buffer * 4),
                          (0, kwargs['height'] - buffer * 4)
                          ]
                draw.polyline(points)
                draw(image)
            with Drawing() as draw:
                draw.stroke_color = Color('black')
                draw.fill_color = Color('white')
                points = [(buffer, kwargs['height'] - buffer * 3),
                          (buffer, kwargs['height'] - buffer),
                          (scale_width + buffer, kwargs['height'] - buffer),
                          (scale_width + buffer, kwargs['height'] - buffer * 3)
                          ]
                draw.polyline(points)
                draw(image)
            with Drawing() as draw:
                draw.font = '/Library/Fonts/Verdana.ttf'
                draw.font_size = 3
                draw.fill_color = Color('black')
                draw.gravity = "south_west"
                draw.text(int(scale_width / 2), buffer, scale_label)
                draw(image)
            image.save(filename=kwargs['filename'])

    def type(self):
        return "scale"


class DefaultRenderer(Renderer):
    def render(self, **kwargs):
        raise NotImplementedError("This method is not yet implemented")

    def type(self):
        return "default"
