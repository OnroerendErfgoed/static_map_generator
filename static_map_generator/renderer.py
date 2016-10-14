# -*- coding: utf-8 -*-
"""
Adapters to help render map layers
"""
# import os
from abc import ABCMeta, abstractmethod
import json
from pyramid.httpexceptions import HTTPNotFound
from pyramid.renderers import JSON
from requests.packages.urllib3.connection import ConnectionError
import requests
import mapnik
# from wand.color import Color
# from wand.display import display
# from wand.image import Image
# from wand.image import Font
from static_map_generator.utils import merge_dicts
# from static_map_generator.utils import convert_wkt_to_geojson, position_figure, define_scale_number

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
        # elif layer_type == "text":
        #     return TextRenderer()
        # elif layer_type == "logo":
        #     return LogoRenderer()
        # elif layer_type == "scale":
        #     return ScaleRenderer()
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
# class TextRenderer(Renderer):
#     def render(self, **kwargs):
#
#         with Image(width=kwargs['width'],
#                    height=kwargs['height']) as image:
#             font = Font(path='/Library/Fonts/Verdana.ttf', size=kwargs['font_size'], color=Color(kwargs['text_color']))
#             image.caption(kwargs['text'], left=0, top=0,
#                           font=font, gravity=kwargs['gravity'])
#             image.save(filename=kwargs['filename'])
#
#     def type(self):
#         return "text"
#
#
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
# class ScaleRenderer(Renderer):
#         #todo: this is just some test implementation!
#     def render(self, **kwargs):
#         if kwargs['epsg']!= 31370:
#             raise NotImplementedError("This method is not yet implemented for epsg other than 31370")
#
#         here = os.path.abspath(os.path.dirname(__file__))
#         path = os.path.join(here, 'fixtures/scalebar.png')
#         with Image(filename=path) as scale_img:
#             # scale_number = str((kwargs['bbox'][2]- kwargs['bbox'][0])/kwargs['divid']) + ' m'
#             # scalebar_width = int(kwargs['width']/kwargs['divid'])
#             # scalebar_height = (scale_img.height*scalebar_width/scale_img.width)
#             # scale_img.resize(width=scalebar_width, height = scalebar_height)
#             scale_number = define_scale_number(kwargs['bbox'][2]- kwargs['bbox'][0], kwargs['width'], kwargs['imagewidth'])
#             scale_img.resize(width=kwargs['imagewidth'], height = kwargs['imageheight'])
#             scale_img.transparentize(1 - kwargs['opacity'])
#             font = Font(path='/Library/Fonts/Verdana.ttf', size=kwargs['font_size'], color=Color('#000000'))
#             scale_img.caption(scale_number, left=0, top=0,
#                           font=font, gravity='center')
#             position_figure(kwargs['width'], kwargs['height'], scale_img, kwargs['gravity'], kwargs['offset'], kwargs['filename'])
#
#
#     def type(self):
#         return "scale"
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
