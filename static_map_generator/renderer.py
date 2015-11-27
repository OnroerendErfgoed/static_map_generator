import os
from abc import ABCMeta, abstractmethod
import json

from pyramid.httpexceptions import HTTPNotFound
from requests import ConnectionError
import requests

import mapnik
from wand.color import Color
from wand.image import Image
from wand.image import Font
from static_map_generator.utils import merge_dicts, convert_wkt_to_geojson


class Renderer():
    __metaclass__ = ABCMeta

    @staticmethod
    def factory(type):
        if type == "wms":
            return WmsRenderer()
        elif type == "wkt":
            return WktRenderer()
        elif type == "geojson":
            return GeojsonRenderer()
        elif type == "text":
            return TextRenderer()
        elif type == "logo":
            return LogoRenderer()
        elif type == "scale":
            return ScaleRenderer()
        elif type == "legend":
            return LegendRenderer()
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
            "srs": "EPSG:" + str(kwargs['epsg']),
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
        with open(kwargs['filename'], 'wb') as im:
                im.write(res.content)

    def type(self):
        return "wms"


class GeojsonRenderer(Renderer):
    def render(self, **kwargs):
        m = mapnik.Map(kwargs['width'], kwargs['height'], '+init=epsg:' + str(kwargs['epsg']))
        s = mapnik.Style()
        r = mapnik.Rule()
        polygon_symbolizer = mapnik.PolygonSymbolizer(mapnik.Color(str(kwargs['color'])))
        polygon_symbolizer.fill_opacity = kwargs['opacity']
        r.symbols.append(polygon_symbolizer)
        line_symbolizer = mapnik.LineSymbolizer(mapnik.Color('rgb(50%,50%,50%)'), 1.0)
        r.symbols.append(line_symbolizer)
        point_symbolizer = mapnik.PointSymbolizer()
        r.symbols.append(point_symbolizer)
        s.rules.append(r)
        m.append_style('My Style', s)
        ds = mapnik.Ogr(string=json.dumps(kwargs['geojson']), layer='OGRGeoJSON')
        layer = mapnik.Layer('wkt', '+init=epsg:' + str(kwargs['epsg']))
        layer.datasource = ds
        layer.styles.append('My Style')
        m.layers.append(layer)
        extent = mapnik.Box2d(kwargs['bbox'][0], kwargs['bbox'][1], kwargs['bbox'][2], kwargs['bbox'][3])
        m.zoom_to_box(extent)
        mapnik.render_to_file(m, str(kwargs['filename']), str(kwargs['filetype']))

    def type(self):
        return "geojson"


class WktRenderer(Renderer):
    def render(self, **kwargs):
        kwargs['geojson'] = convert_wkt_to_geojson(kwargs['wkt'])
        GeojsonRenderer().render(**kwargs)

    def type(self):
        return "wkt"


class TextRenderer(Renderer):
    def render(self, **kwargs):
        with Image(width=kwargs['width'],
                   height=kwargs['height']) as image:
            font = Font(path='/Library/Fonts/Verdana.ttf', size=kwargs['font_size'], color=Color(kwargs['text_color']))
            image.caption(kwargs['text'], left=0, top=0, width=kwargs['width'] - 10, height=kwargs['height'] - 5,
                          font=font, gravity='center')
            image.save(filename=kwargs['filename'])

    def type(self):
        return "text"


class LogoRenderer(Renderer):
    def render(self, **kwargs):

        response = requests.get(kwargs['url'], stream=True)
        # img = Image.open(StringIO(response.content))
        with Image(blob=response.content) as img:
            img.resize(width=kwargs['width'], height=kwargs['height'])
            img.transparentize(1 - kwargs['opacity'])
            img.save(filename=kwargs['filename'])

    def type(self):
        return "logo"


class ScaleRenderer(Renderer):
    def render(self, **kwargs):
        #todo: this is just some test implementation!
        here = os.path.abspath(os.path.dirname(__file__))
        path = os.path.join(here, 'scale.png')
        with Image(filename=path) as img:
            width = kwargs['width']
            scalewidth = width/10
            scaleheight = img.height*scalewidth/img.width
            img.resize(width=scalewidth, height =scaleheight)
            img.save(filename=kwargs['filename'])

    def type(self):
        return "scale"


class LegendRenderer(Renderer):
    def render(self, **kwargs):
        raise NotImplementedError("This method is not yet implemented")

    def type(self):
        return "legend"

class DefaultRenderer(Renderer):
    def render(self, **kwargs):
        raise NotImplementedError("This method is not yet implemented")

    def type(self):
        return "default"
