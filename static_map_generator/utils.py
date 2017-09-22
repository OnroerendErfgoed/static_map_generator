
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


def calculate_scale(map_scale, map_width):
    """
    Calculates the image scale with in pixels together with the scale label
    using map scale (meters per pixels) and map width (pixels)
    """
    image_width_meter = round(map_scale * float(map_width))
    scale_num_guess = str(int(round(image_width_meter * 0.2)))
    scale_num = int(2 * round(float(int(scale_num_guess[0])) / 2)) * 10 ** (len(scale_num_guess[1:]))
    scale_num = scale_num if scale_num else 1 * 10 ** (len(scale_num_guess[1:]))
    scale_width = round(scale_num / map_scale)
    scale_label = "{} m".format(scale_num) if scale_num < 1000 else "{} km".format(scale_num/1000)

    return scale_width, scale_label


