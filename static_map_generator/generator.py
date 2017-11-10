import logging
import os
import tempdir
import mapnik
import base64
from static_map_generator.renderer import Renderer
from static_map_generator.utils import merge_dicts, rescale_bbox


log = logging.getLogger(__name__)


class Generator:

    @staticmethod
    def generate(config):
        """
        Creates a map based on a configuration file
        :param config
        :return:
        """

        # generate map
        mapnik_map = mapnik.Map(config['params']['width'], config['params']['height'], '+init=epsg:31370')
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
        s.rules.append(r)
        mapnik_map.append_style('default', s)
        s = mapnik.Style()
        r = mapnik.Rule()
        point_symbolizer = mapnik.PointSymbolizer()
        point_symbolizer.file = os.path.abspath(os.path.dirname(__file__)) + '/fixtures/pointer.svg'
        r.symbols.append(point_symbolizer)
        s.rules.append(r)
        mapnik_map.append_style('point', s)

        # render layers
        layers = [layer for layer in config['layers'] if layer['type'] in ['geojson']]
        for idx, layer in enumerate(layers):
            renderer = Renderer.factory(layer['type'])
            layer['idx'] = idx
            kwargs = merge_dicts(config['params'], layer)
            try:
                rendered_layer = renderer.render(**kwargs)
                rendered_layer.styles.append('default')
                mapnik_map.layers.append(rendered_layer)
            except Exception as e:
                log.error('Following layer could not be rendered: ' + str(idx))
                log.error(e, exc_info=True)
                raise

        # bbox is the given bbox or the bbox of the layers with a buffer value
        if config['params'].get('bbox') is None:
            mapnik_map.zoom_all()
            extend = mapnik_map.envelope()
            min_width = int(min(extend.maxx - extend.minx, extend.maxy - extend.miny))
            min_width_param = max(len(str(min_width)) - 1, 2)
            extend.width(extend.width() + 10 ** min_width_param)
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
                log.error('Background wms could not be rendered')
                log.error(e, exc_info=True)
                raise

        im = mapnik.Image(mapnik_map.width, mapnik_map.height)
        mapnik.render(mapnik_map, im)
        filename = os.path.join(str(config['params']['tempdir']), "result")
        im.save(filename, 'png')

        # add text
        text_layers = [layer for layer in config['layers'] if layer['type'] == 'text']
        for text_layer in text_layers:
            renderer = Renderer.factory('text')
            config['params']['filename'] = filename
            kwargs = merge_dicts(config['params'], text_layer)
            try:
                renderer.render(**kwargs)
            except Exception as e:
                log.error('Text could not be rendered')
                log.error(e, exc_info=True)
                raise

        # add scale
        renderer = Renderer.factory('scale')
        config['params']['filename'] = filename
        scale = {
            "map_scale": mapnik_map.scale(),
            "gravity": "south_west",
            "font_size": 3
        }
        kwargs = merge_dicts(config['params'], scale)
        try:
            renderer.render(**kwargs)
        except Exception as e:
            log.error('Scale could not be rendered')
            log.error(e, exc_info=True)
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
