import json

import os

from shapely.geometry import shape
from shapely.ops import unary_union
from shapely.wkt import loads
from wand.color import Color
from wand.exceptions import WandException
from wand.image import Font
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

def position_figure(width, height, figure, gravity, offset, filename):
    offset = offset.split(",")
    offset_left = int(offset[0])
    offset_top = int(offset[1])

    if gravity == 'north_west':
        left = 0 + offset_left
        top = 0 + offset_top
    elif gravity == 'north_east':
        left = width - figure.width - offset_left
        top = 0 + offset_top
    elif gravity == 'south_west':
        left = 0 + offset_left
        top = height - figure.height - offset_top
    elif gravity == 'south_east':
        left = width - figure.width - offset_left
        top = height - figure.height - offset_top
    elif gravity == 'center':
        left = width/2 - figure.width/2 + offset_left
        top = height/2 - figure.height/2 + offset_top

    with Image(width=width, height=height) as img:
        img.composite(figure, left=left, top=top)
        img.save(filename=filename)

def define_scale_number(real_width, width, scalebar_width):
    scale_number = float(real_width*scalebar_width)/width
    if scale_number/1000 > 5:
        scale_number = str(int(scale_number/1000)) + ' km'
    else:
        scale_number = str(int(scale_number)) + ' m'
    return scale_number

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

