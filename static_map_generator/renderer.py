# -*- coding: utf-8 -*-
"""
Adapters to help render map layers
"""
import os
from abc import ABCMeta, abstractmethod
import json
from pyramid.httpexceptions import HTTPNotFound
from pyramid.renderers import JSON
from requests.packages.urllib3.connection import ConnectionError
import requests
import mapnik
from wand.color import Color
# from wand.display import display
from wand.image import Image
from wand.image import Font
from static_map_generator.utils import merge_dicts
from wand.drawing import Drawing

json_item_renderer = JSON()


class Renderer(object):
    __metaclass__ = ABCMeta

    @staticmethod
    def factory(layer_type):
        if layer_type == "wms":
            return WmsRenderer()
        # elif layer_type == "wkt":
        #     return WktRenderer()
        elif layer_type == "geojson":
            return GeojsonRenderer()
        elif layer_type == "text":
            return TextRenderer()
        # elif layer_type == "logo":
        #     return LogoRenderer()
        # elif layer_type == "legend":
        #     return LegendRenderer()
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
            "format": "image/" + kwargs['filetype'],
            "service": "WMS",
            "version": "1.1.0",
            "request": "GetMap",
            "styles": '',
            #"srs": "EPSG:" + str(kwargs['epsg']),
            "srs": "EPSG:31370",
            "bbox": str(kwargs['bbox'][0]) + "," + str(kwargs['bbox'][1]) + "," + str(kwargs['bbox'][2]) + "," + str(kwargs['bbox'][3]),
            "width": kwargs['width'],
            "height": kwargs['height']
        }
        params = merge_dicts(kwargs, params)
        try:
            res = requests.get(kwargs['url'], params=params)
        except ConnectionError as e:
            raise ConnectionError("Request could not be executed - Request: %s - Params: %s" % (kwargs['url'], params))
        if res.status_code == 404:
            raise HTTPNotFound("Service not found (status_code 404) - Request: %s - Params: %s" % (kwargs['url'], params))
        if res.content[2:5]=='xml':
            raise ValueError("Exception occured - Request: %s - Params: %s -  Reason: %s" % (kwargs['url'], params, res.content))
        return res.content

    def type(self):
        return "wms"


class GeojsonRenderer(Renderer):
    def render(self, **kwargs):
        # fix to create valid geojson from contour
        geojson = { "type": "Feature", "properties": {}, "geometry": {}}
        geojson['geometry'] = kwargs['geojson']
        ds = mapnik.MemoryDatasource()
        feature = mapnik.Feature.from_geojson(json.dumps(geojson), mapnik.Context())
        ds.add_feature(feature)
        layer = mapnik.Layer('geojson' + str(kwargs['idx']), '+init=epsg:' + str(kwargs['epsg']))
        layer.datasource = ds
        return layer

    def type(self):
        return "geojson"


# class WktRenderer(Renderer):
#     def render(self, **kwargs):
#         kwargs['geojson'] = convert_wkt_to_geojson(kwargs['wkt'])
#         GeojsonRenderer().render(**kwargs)
#
#     def type(self):
#         return "wkt"
#
#
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


# class LogoRenderer(Renderer):
#     def render(self, **kwargs):
#
#         response = requests.get(kwargs['url'], stream=True)
#         with Image(blob=response.content) as img:
#             img.resize(width=kwargs['imagewidth'], height=kwargs['imageheight'])
#             img.transparentize(1 - kwargs['opacity'])
#             position_figure(kwargs['width'], kwargs['height'], img, kwargs['gravity'], kwargs['offset'],  kwargs['filename'])
#
#     def type(self):
#         return "logo"
#
#
# class LegendRenderer(Renderer):
#     def render(self, **kwargs):
#         raise NotImplementedError("This method is not yet implemented")
#
#     def type(self):
#         return "legend"
#

class DefaultRenderer(Renderer):
    def render(self, **kwargs):
        raise NotImplementedError("This method is not yet implemented")

    def type(self):
        return "default"
