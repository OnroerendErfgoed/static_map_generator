import logging
import os
import tempdir
import mapnik
import base64
from static_map_generator.renderer import Renderer
from static_map_generator.utils import merge_dicts


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
        # polygon_symbolizer = mapnik.PolygonSymbolizer(mapnik.Color(str(kwargs['color'])))
        polygon_symbolizer = mapnik.PolygonSymbolizer(mapnik.Color('steelblue'))
        # polygon_symbolizer.fill_opacity = kwargs['opacity']
        polygon_symbolizer.fill_opacity = 0.5
        r.symbols.append(polygon_symbolizer)
        line_symbolizer = mapnik.LineSymbolizer(mapnik.Color('rgb(50%,50%,50%)'), 1.0)
        r.symbols.append(line_symbolizer)
        point_symbolizer = mapnik.PointSymbolizer()
        r.symbols.append(point_symbolizer)
        s.rules.append(r)
        mapnik_map.append_style('default', s)

        # render layers
        for idx, layer in enumerate(config['layers']):
            renderer = Renderer.factory(layer['type'])
            layer['idx'] = idx
            # layer['filetype'] = 'png'
            # layer['filename'] = os.path.join(temp.name, str(idx) + '.' + layer['filetype'])
            kwargs = merge_dicts(config['params'], layer)
            try:
                rendered_layer = renderer.render(**kwargs)
                if renderer.type() == 'wms':
                    # mapnik_map.background_image = rendered_layer
                    background = os.path.join(str(config['params']['tempdir']), "background.png")
                    with open(background, 'wb') as im:
                            im.write(rendered_layer)
                    mapnik_map.background_image = background

                else:
                    rendered_layer.styles.append('default')
                    mapnik_map.layers.append(rendered_layer)
            except NotImplementedError as e:
                log.warning("Layertype is not yet implemented: " + e.message)
                pass

            except Exception as e:
                log.error('Following layer could not be rendered: ' + str(idx) + ' -->message: ' + e.message)
                raise

        extent = mapnik.Box2d(config['params']['bbox'][0], config['params']['bbox'][1],
                              config['params']['bbox'][2], config['params']['bbox'][3])
        mapnik_map.zoom_to_box(extent)
        # mapnik.render_to_file(m, str(kwargs['filename']), str(kwargs['filetype']))

        im = mapnik.Image(mapnik_map.width, mapnik_map.height)
        mapnik.render(mapnik_map, im)
        filename = os.path.join(str(config['params']['tempdir']), "result")
        im.save(filename, 'png')

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
        # with open(image_file, 'rb') as f:
        #     return f.read()
