import logging
import os
import tempdir
import mapnik
import base64
from static_map_generator.renderer import Renderer
from static_map_generator.utils import merge_dicts, rescale_bbox


log = logging.getLogger(__name__)


class Generator():

    @staticmethod
    def generate(config):
        """
        Creates a map based on a configuration file
        :param config
        :return:
        """

        # generate map
        mapnik_map = mapnik.Map(config['params']['width'], config['params']['height'],
                                '+init=epsg:' + str(config['params']['epsg']))
        mapnik_map.background = mapnik.Color('white')

        s = mapnik.Style()
        r = mapnik.Rule()
        polygon_symbolizer = mapnik.PolygonSymbolizer()
        polygon_symbolizer.fill = mapnik.Color('steelblue')
        polygon_symbolizer.fill_opacity = 0.5
        r.symbols.append(polygon_symbolizer)
        line_symbolizer = mapnik.LineSymbolizer()
        line_symbolizer.fill = mapnik.Color('rgb(50%,50%,50%)')
        r.symbols.append(line_symbolizer)
        point_symbolizer = mapnik.PointSymbolizer()
        r.symbols.append(point_symbolizer)
        s.rules.append(r)
        mapnik_map.append_style('default', s)

        layers = [layer for layer in config['layers'] if layer['type'] not in ['wms', 'text']]
        # render layers
        for idx, layer in enumerate(layers):
            renderer = Renderer.factory(layer['type'])
            layer['idx'] = idx
            kwargs = merge_dicts(config['params'], layer)
            try:
                rendered_layer = renderer.render(**kwargs)
                rendered_layer.styles.append('default')
                mapnik_map.layers.append(rendered_layer)
            except NotImplementedError as e:
                log.warning("Layertype is not yet implemented: " + e.message)
                pass

            except Exception as e:
                log.error('Following layer could not be rendered: ' + str(idx) + ' -->message: ' + e.message)
                raise

        # bbox is the given bbox or the bbox of the layers with a buffer value
        if not config['params']['bbox']:
            mapnik_map.zoom_all()
            min_extend = mapnik_map.envelope()
            mapnik_map.buffer_size = int(
                (max(min_extend.maxx - min_extend.minx, min_extend.maxy - min_extend.miny)) * 0.5)
            extend = mapnik_map.buffered_envelope()
            bbox_layers = [extend.minx, extend.miny, extend.maxx, extend.maxy]
        else:
            bbox_layers = config['params']['bbox']
            extend = mapnik.Box2d(bbox_layers[0], bbox_layers[1], bbox_layers[2], bbox_layers[3])
        mapnik_map.zoom_to_box(extend)

        # render background
        background_layers = [layer for layer in config['layers'] if layer['type'] == 'wms']
        background = background_layers[0] if len(background_layers) > 0 else None
        if background:
            # printing map to image works differently for wms in comparison to Mapnik rendering
            # rescaling of the bbox is necessary to avoid deformations of the background image
            bbox = rescale_bbox(config['params']['height'], config['params']['width'], bbox_layers)
            config['params']['bbox'] = bbox
            mapnik_map.zoom_to_box(mapnik.Box2d(bbox[0], bbox[1], bbox[2], bbox[3]))
            # rendering the background image
            renderer = Renderer.factory('wms')
            kwargs = merge_dicts(config['params'], background)
            try:
                rendered_layer = renderer.render(**kwargs)
                background = os.path.join(str(config['params']['tempdir']), "background.png")
                with open(background, 'wb') as im:
                    im.write(rendered_layer)
                mapnik_map.background_image = background
            except Exception as e:
                log.error('Background wms could not be rendered: -->message: ' + e.message)
                raise

        im = mapnik.Image(mapnik_map.width, mapnik_map.height)
        mapnik.render(mapnik_map, im)
        filename = os.path.join(str(config['params']['tempdir']), "result")
        im.save(filename, 'png')

        # from static_map_generator.utils import convert_png_to_svg
        # filename_svg = convert_png_to_svg(config['params']['width'], config['params']['height'], filename)

        # add text
        text_layers = [layer for layer in config['layers'] if layer['type'] == 'text']
        text = text_layers[0] if len(text_layers) > 0 else None
        if text:
            renderer = Renderer.factory('text')
            config['params']['filename'] = filename
            kwargs = merge_dicts(config['params'], text)
            try:
                renderer.render(**kwargs)
            except Exception as e:
                log.error('Text could not be rendered: -->message: ' + e.message)
                raise

        # add scale
        renderer = Renderer.factory('text')
        config['params']['filename'] = filename
        scale = {
            "text": "Schaal 1:{}".format(int(mapnik_map.scale_denominator())),
            "gravity": "south_west",
            "font_size": 3
        }
        kwargs = merge_dicts(config['params'], scale)
        try:
            renderer.render(**kwargs)
        except Exception as e:
            log.error('Scale could not be rendered: -->message: ' + e.message)
            raise

        return filename

    @staticmethod
    def generate_stream(config):
        temp = tempdir.TempDir()
        config['params']['tempdir'] = temp.name
        image_file = Generator.generate(config)

        with open(image_file, 'rb') as f:
            return f.read()

    @staticmethod
    def generate_base64(config):
        temp = tempdir.TempDir()
        config['params']['tempdir'] = temp.name
        image_file = Generator.generate(config)

        with open(image_file, "rb") as image_file:
            return base64.b64encode(image_file.read())