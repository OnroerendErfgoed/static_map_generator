import unittest
from static_map_generator.utils import convert_filetype


class UtilsTests(unittest.TestCase):

    def test_convert_filetype(self):
        convert_filetype('logo.png', 'logo.jpg', 'jpg')
        convert_filetype('overviewmap.png', 'overviewmap.jpg', 'jpg')
        convert_filetype('overviewmap.png', 'overviewmap.pdf', 'pdf')
