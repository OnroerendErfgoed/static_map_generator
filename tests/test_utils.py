import os
import unittest
import tempdir
from wand.image import Image
from static_map_generator.utils import convert_filetype, combine_layers


class UtilsTests(unittest.TestCase):

    def setUp(self):
        self.tempdir = tempdir.TempDir()
        self.here = os.path.abspath(os.path.dirname(__file__))

    def tearDown(self):
        pass

    def test_convert_filetype(self):
        file_path = os.path.join(self.tempdir.name, 'filepath.jpg')
        convert_filetype(os.path.join(self.here, "31370.png"), file_path, 'jpg')
        self.assertTrue(os.path.isfile(file_path))
        image = Image(filename=file_path)
        self.assertIsInstance(image, Image)
        self.assertEquals(image.mimetype, 'image/jpeg')

    def test_combine_images(self):
        file_path = os.path.join(self.tempdir.name, 'filename.png')
        images = [os.path.join(self.here, "31370.png"), os.path.join(self.here, "4326.png")]
        combine_layers(images, file_path)
        self.assertTrue(os.path.isfile(file_path))
        image = Image(filename=file_path)
        self.assertIsInstance(image, Image)


