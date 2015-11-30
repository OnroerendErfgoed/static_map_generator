import json
from shapely.geometry import shape
from shapely.ops import unary_union
from shapely.wkt import loads
from wand.exceptions import WandException
from wand.image import Image
import geojson
import shapely.wkt

def combine_layers(images, filename):
    combo = None
    for index, im in enumerate(images):
        if not isinstance(combo, Image):
            combo = Image(filename=im)
        if index == len(images) - 1:
            break
        else:
            im2 = images[index + 1]
            im2 = Image(filename=im2)
            combo.composite(im2, left=0, top=0)
    combo.save(filename=filename)
    combo.close()

# def combine_layers(images):
# from PIL import Image as PILImage
#     combo = None
#     for index,im in enumerate(images):
#         if not combo:
#             combo = PILImage.open(im) if isinstance(im, str) else im
#             combo = combo.convert(mode='RGBA')
#         if index == len(images)-1:
#             break
#         else:
#             im2 = images[index+1]
#             im2 = PILImage.open(im2) if isinstance(im2, str) else im2
#             im2 = im2.convert(mode='RGBA')
#             combo = PILImage.alpha_composite(combo, im2)
#
#     combo.save("result.png")

# def create_buffer(wkt, buffer):
#     geom = loads(wkt)
#     return geom.buffer(buffer)

def position_figure(width, height, figure, gravity, filename):

    if gravity == 'north_west':
        left = 0
        top = 0
    elif gravity == 'north_east':
        left = width - figure.width
        top = 0
    elif gravity == 'south_west':
        left = 0
        top = height - figure.height
    elif gravity == 'south_east':
        left = width - figure.width
        top = height - figure.height
    elif gravity == 'center':
        left = width/2 - figure.width/2
        top = height/2 - figure.height/2

    with Image(width=width, height=height) as img:
        img.composite(figure, left=left, top=top)
        img.save(filename=filename)


def merge_dicts(*dict_args):
    '''
    Given any number of dicts, shallow copy and merge into a new dict,
    precedence goes to key value pairs in latter dicts.
    '''
    result = {}
    for dictionary in dict_args:
        result.update(dictionary)
    return result


def convert_filetype(filename_ori, filename_res, filetype):
    original = Image(filename=filename_ori)
    with original.convert(filetype) as converted:
        converted.save(filename=filename_res)

def convert_geojson_to_wkt(value):
    s = json.dumps(value)
    g1 = geojson.loads(s)
    g2 = shape(g1)
    return g2.wkt


def convert_wkt_to_geojson(value):
    g1 = shapely.wkt.loads(value)
    g2 = geojson.Feature(geometry=g1, properties={})
    return g2.geometry

