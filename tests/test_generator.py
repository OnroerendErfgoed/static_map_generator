import unittest
import tempdir
from wand.image import Image
import static_map_generator.generator
import os.path

class MapMakerTests(unittest.TestCase):

    def setUp(self):
        self.tempdir = tempdir.TempDir()

    def tearDown(self):
        pass

    def test_static_map_generator(self):
        file_path = os.path.join(self.tempdir.name, 'test.png')
        width = 500
        height = 500
        simple_config = {
            'params': {
                'filename': file_path,
                'epsg': 31370,
                'filetype': 'png',
                'width': width,
                'height': height,
                'bbox': [145000, 195000, 165000, 215000]
            },
            'layers':
                [{'layer': {
                    'type': 'text',
                    'name': 'text.png',
                    'text': 'This is a test',
                    'color': '#FF3366',
                    'borderwidth': 0,
                    'font_size': 24,
                    'text_color': '#FF3366'
                }
                  }
                 ]
        }
        static_map_generator.generator.Generator.generate(simple_config)
        self.assertTrue(os.path.isfile(file_path))
        image = Image(filename=file_path)
        self.assertEqual(image.width, width)
        self.assertEqual(image.height, height)