from abc import ABCMeta, abstractmethod

from requests import ConnectionError
import requests

from _mapnik import Box2d
import mapnik
from wand.color import Color
from wand.image import Image
from wand.image import Font
from static_map_generator.utils import merge_dicts


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
        # filename, url, layers, filetype, epsg, width, height, bbox
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
            raise Exception("Request could not be executed - Request: %s - Params: %s" % (kwargs['url'], params))
        if res.status_code == 404:
            raise Exception("Service not found (status_code 404) - Request: %s - Params: %s" % (kwargs['url'], params))
        if res.content[2:5]=='xml':
            raise Exception("Exception occured - Request: %s - Params: %s -  Reason: %s" % (kwargs['url'], params, res.content))
        with open(kwargs['filename'], 'wb') as im:
                im.write(res.content)


    def type(self):
        return "wms"

class WktRenderer(Renderer):

    def render(self, **kwargs):
        m = mapnik.Map(kwargs['width'], kwargs['height'], '+init=epsg:' + str(kwargs['epsg']))
        s = mapnik.Style()
        r = mapnik.Rule()
        polygon_symbolizer = mapnik.PolygonSymbolizer(mapnik.Color(kwargs['color']))
        polygon_symbolizer.fill_opacity = kwargs['opacity']
        r.symbols.append(polygon_symbolizer)
        line_symbolizer = mapnik.LineSymbolizer(mapnik.Color('rgb(50%,50%,50%)'), 1.0)
        r.symbols.append(line_symbolizer)
        s.rules.append(r)
        m.append_style('My Style', s)
        csv_string = '''
         wkt,Name
        "%s","test"
        ''' % kwargs['wkt']
        ds = mapnik.Datasource(**{"type": "csv", "inline": csv_string})
        layer = mapnik.Layer('world', '+init=epsg:' + str(kwargs['epsg']))
        layer.datasource = ds
        layer.styles.append('My Style')
        m.layers.append(layer)
        extent = Box2d(kwargs['bbox'][0], kwargs['bbox'][1], kwargs['bbox'][2], kwargs['bbox'][3])
        m.zoom_to_box(extent)
        mapnik.render_to_file(m, kwargs['filename'], kwargs['filetype'])

    def type(self):
        return "wkt"


class TextRenderer(Renderer):
    def render(self, **kwargs):
        with Image(width=kwargs['width'] - 2 * kwargs['borderwidth'],
                   height=kwargs['height'] - 2 * kwargs['borderwidth']) as image:
            # image.border(Color(bordercolor),borderwidth,borderwidth)
            font = Font(path='/Library/Fonts/Verdana.ttf', size=kwargs['font_size'], color=Color(kwargs['text_color']))
            image.caption(kwargs['text'], left=0, top=0, width=kwargs['width'] - 10, height=kwargs['height'] - 5,
                          font=font, gravity='center')
            image.save(filename=kwargs['filename'])

    def type(self):
        return "text"

class LogoRenderer(Renderer):
    def render(self, **kwargs):
        with Image(filename=kwargs['path']) as img:
            img.resize(width=kwargs['width'], height=kwargs['height'])
            img.transparentize(0.9)
            img.save(filename=kwargs['filename'])

    def type(self):
        return "logo"


class GeojsonRenderer(Renderer):
    def render(self, **kwargs):
        raise NotImplementedError("This method is not yet implemented")

    def type(self):
        return "geojson"


class ScaleRenderer(Renderer):
    def render(self, **kwargs):
        raise NotImplementedError("This method is not yet implemented")

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
