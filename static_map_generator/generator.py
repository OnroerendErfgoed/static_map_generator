import logging
import warnings
import os
import tempdir
from static_map_generator.renderer import Renderer
from static_map_generator.utils import combine_layers, merge_dicts, convert_filetype


log = logging.getLogger(__name__)

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
        if not 'filename' in config['params']:
            config['params']['filename'] = os.path.join(temp.name, "result")

        #render layers
        idx = 0
        for layer in config['layers']:
            idx = idx + 1
            renderer = Renderer.factory(layer['type'])
            layer['filetype'] = 'png'
            layer['filename'] = os.path.join(temp.name, str(idx) + '.' + layer['filetype'])

            kwarguments = merge_dicts(config['params'], layer)
            try:
                renderer.render(**kwarguments)
                images.append(layer['filename'])

            except Exception as e:
                log.error('Following layer could not be rendered: ' + str(idx) + ' -->message: ' + e.message)
                raise
        #combine individual layers
        temp_combined = os.path.join(temp.name, 'combined')
        combine_layers(images[::-1], temp_combined)

        #convert filetype
        convert_filetype(temp_combined, config['params']['filename'], config['params']['filetype'])
        return config

    @staticmethod
    def generateStream(config):
        temp = tempdir.TempDir()
        config['params']['filename'] = os.path.join(temp.name, "result")
        config = Generator.generate(config)
        with open(config['params']['filename'],'rb') as f:
            return f.read()