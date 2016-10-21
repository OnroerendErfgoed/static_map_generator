# import json
#
# import os
#
# from shapely.geometry import shape
# from shapely.ops import unary_union
# from shapely.wkt import loads
# from wand.color import Color
# from wand.exceptions import WandException
# from wand.image import Font
from wand.image import Image
# import geojson
# import shapely.wkt


# def combine_layers(images, filename):
#     combo = None
#     for index, im in enumerate(images):
#         if not isinstance(combo, Image):
#             combo = Image(filename=im)
#         if index == len(images) - 1:
#             break
#         else:
#             im2 = images[index + 1]
#             im2 = Image(filename=im2)
#             combo.composite(im2, left=0, top=0)
#     combo.save(filename=filename)
#     combo.close()

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


def merge_dicts(*dict_args):
    """
    Given any number of dicts, shallow copy and merge into a new dict,
    precedence goes to key value pairs in latter dicts.
    """
    result = {}
    for dictionary in dict_args:
        result.update(dictionary)
    return result


def rescale_bbox(height, width, bbox):
    """
    In case of metric coordinates:
        Increase either longitude or either latitude (on both min and max values)
        to obtain the same scale dimension (longitude/latitude) of the image scale dimensions (height/width)
    :param height: height of the image
    :param width: width of the image
    :param bbox: bbox of the map
    :return:
    """

    x1, y1, x2, y2 = bbox
    scale_image = float(height)/float(width)
    scale_bbox = float(y2-y1)/float(x2-x1)
    if scale_image < scale_bbox:
        x = (((y2-y1)/scale_image) - x2 + x1)/2
        return [x1 - x, y1, x2 + x, y2]
    elif scale_image > scale_bbox:
        y = ((scale_image * (x2-x1)) - y2 + y1)/2
        return [x1, y1 - y, x2, y2 + y]
    else:
        return bbox

#
# def convert_filetype(filename_ori, filename_res, filetype):
#     original = Image(filename=filename_ori)
#     with original.convert(filetype) as converted:
#         converted.save(filename=filename_res)
#
#
# def convert_geojson_to_wkt(value):
#     s = json.dumps(value)
#     g1 = geojson.loads(s)
#     g2 = shape(g1)
#     return g2.wkt
#
#
# def convert_wkt_to_geojson(value):
#     g1 = shapely.wkt.loads(value)
#     g2 = geojson.Feature(geometry=g1, properties={})
#     return g2.geometry

