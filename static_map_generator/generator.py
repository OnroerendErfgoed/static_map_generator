import warnings
import os
import tempdir
from static_map_generator.renderer import Renderer
from static_map_generator.utils import combine_layers, merge_dicts, convert_filetype


class Generator():

    @staticmethod
    def generate(config):
        '''
        Creates a map based on a configuration file
        :param config
        :return:
        '''

        temp = tempdir.TempDir()
        images = []

        #render layers
        for l in config['layers']:
            layer = l['layer']
            renderer = Renderer.factory(layer['type'])
            layer['filename'] = os.path.join(temp.name, layer['name'])
            layer['filetype'] = 'png'

            kwarguments = merge_dicts(config['params'], layer)
            try:
                renderer.render(**kwarguments)
                images.append(layer['filename'])
            except Exception as e:
                warnings.warn(
            'Following layer could not be rendered:' + layer['name'] + 'message: ' + e.message,
            UserWarning
        )
        #combine individual layers
        temp_combined = os.path.join(temp.name, 'combined')
        combine_layers(images[::-1], temp_combined)

        #convert filetype
        convert_filetype(temp_combined, config['params']['filename'], config['params']['filetype'])
        return