import os
import unittest
import tempdir
from wand.image import Image
from static_map_generator.utils import convert_filetype, combine_layers


class UtilsTests(unittest.TestCase):

    def setUp(self):
        self.tempdir = tempdir.TempDir()

    def tearDown(self):
        pass

    # def test_convert_filetype(self):
    #     file_path = os.path.join(self.tempdir.name, 'filepath.jpg')
    #     convert_filetype('31370.png', file_path, 'jpg')

    # def test_combine_images(self):
    #     file_path = os.path.join(self.tempdir.name, 'filename.png')
    #     images = ["31370.png", "4326.png"]
    #     combine_layers(images, file_path)
    #     self.assertTrue(os.path.isfile(file_path))
    #     image = Image(filename=file_path)
    #     self.assertIsInstance(image, Image)


