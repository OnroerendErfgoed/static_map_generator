# -*- coding: utf-8 -*-
import colander
import rfc3987
from shapely import wkt, geometry
import json
import geojson


class ValidationFailure(Exception):
    """
    Custom Exception for data validation errors.
    """

    def __init__(self, msg, errors):
        self.msg = msg
        self.errors = errors


def uri_validator(node, uri):
    """
    URL validator rfc3987 is used to check if a URL is correct (https://pypi.python.org/pypi/rfc3987/).

    :param node: The schema node to which this exception relates.
    :param uri: Uri to validate.
    """
    if not rfc3987.match(uri, rule='URI'):
        raise colander.Invalid(node, '{0} is geen geldige URI.'.format(uri))


def wkt_validator(node, wkt_input):
    """
    Shapely WKT validator.

    :param node: The schema node to which this exception relates.
    :param wkt_input: WKT to validate.
    """
    try:
        wkt.loads(wkt_input)
    except Exception:
        raise colander.Invalid(
            node,
            "Could not parse wkt {}".format(wkt_input)
        )


def geojson_validator(node, geojson_input):
    """
    Geojson/Shapely geojson validator.

    :param node: The schema node to which this exception relates.
    :param geojson_input: Geojson to validate.
    """
    try:
        geojson_dump = json.dumps(geojson_input)
        geojson_load = geojson.loads(geojson_dump)
        geometry.shape(geojson_load)
    except Exception:
        raise colander.Invalid(
            node,
            "Could not parse geojson {}".format(geojson_input)
        )


def string_validator(node, value):
    """
    String validator.

    :param node: The schema node to which this exception relates.
    :param value: Value to validate.
    """
    if not isinstance(value, (str, unicode)) or len(value) == 0:
        raise colander.Invalid(
            node,
            "{} is not a valid sting".format(value)
        )


def number_validator(node, value):
    """
    Number validator.

    :param node: The schema node to which this exception relates.
    :param value: Value to validate.
    """
    if not isinstance(value, (int, float, long)):
        raise colander.Invalid(
            node,
            "{} is not a valid number".format(value)
        )
    

def scale_validator(node, value):
    """
    Scale validator.

    :param node: The schema node to which this exception relates.
    :param value: Value to validate.
    """
    if not isinstance(value, (float, long)) or value > 1 or 0 > value:
        raise colander.Invalid(
            node,
            "{} is not a valid scale number (1 > value > 0)".format(value)
        )


def gravity_validator(node, value):
    """
    Gravity validator

    :param node: The schema node to which this exception relates.
    :param value: Value to validate.
    """
    if value not in ['center', 'north_west', 'north_east', 'south_west', 'south_east']:
        raise colander.Invalid(
            node,
            "{} is not one of the following gravities: 'center', 'north_west', 'north_east', 'south_west', 'south_east'".format(value)
        )


def required_validator(param, type, node, cstruct, validator=None):
    """
    Param is required in cstruct for type in node.
    Validates the param with validator (if provided).

    :param param: Required param.
    :param type: The layer type (wms', 'wkt', 'geojson', 'text', 'logo', 'scale' or 'legend').
    :param node: The schema node to which this exception relates.
    :param cstruct: The json object.
    :param validator: The validator function.
    """
    if param not in cstruct:
        raise colander.Invalid(
            node,
            "{0} is required for {1} configuration".format(param, type)
        )
    if validator is not None:
        validator(node, cstruct[param])


def optional_validator(param, default, node, cstruct, validator=None):
    """
    Param is optional in cstruct with a default value.

    :param param: Optional param.
    :param type: The default value.
    :param node: The schema node to which this exception relates.
    :param cstruct: The json object.
    :param validator: The validator function.
    """
    cstruct[param] = cstruct[param] if param in cstruct else default
    if validator is not None:
        validator(node, cstruct[param])
        

class LayerSchemaNode(colander.MappingSchema):
    title = 'layer'

    def schema_type(self, **kw):
        return colander.Mapping(unknown='preserve')

    type = colander.SchemaNode(
            colander.String(),
            validator=colander.OneOf(['wms', 'wkt', 'geojson', 'text', 'logo', 'scale', 'legend'])
    )

    def validator(self, node, cstruct):
        if cstruct['type'] == 'wms':
            required_validator('url', 'wms', node, cstruct, uri_validator)
            required_validator('layers', 'wms', node, cstruct, string_validator)
        elif cstruct['type'] == 'wkt':
            required_validator('wkt', 'wkt', node, cstruct, wkt_validator)
            optional_validator('color', 'steelblue', node, cstruct, string_validator)
            optional_validator('opacity', 0.5, node, cstruct, scale_validator)
        elif cstruct['type'] == 'geojson':
            required_validator('geojson', 'geojson', node, cstruct, geojson_validator)
            optional_validator('color', 'steelblue', node, cstruct, string_validator)
            optional_validator('opacity', 0.5, node, cstruct, scale_validator)
        elif cstruct['type'] == 'text':
            required_validator('text', 'text', node, cstruct, string_validator)
            optional_validator('text_color', '#000000', node, cstruct, string_validator)
            optional_validator('gravity', 'center', node, cstruct, gravity_validator)
            optional_validator('font_size', 10, node, cstruct, number_validator)
        elif cstruct['type'] == 'logo':
            required_validator('url', 'logo', node, cstruct, uri_validator)
            required_validator('imagewidth', 'logo', node, cstruct, number_validator)
            required_validator('imageheight', 'logo', node, cstruct, number_validator)
            optional_validator('opacity', 1, node, cstruct, scale_validator)
            optional_validator('gravity', 'south_east', node, cstruct, string_validator)
            optional_validator('offset', '0,0', node, cstruct, string_validator)
        # elif cstruct['type'] == 'scale':
        #     required_validator('imagewidth', 'logo', node, cstruct, number_validator)
        #     required_validator('imageheight', 'logo', node, cstruct, number_validator)
        #     optional_validator('opacity', 1, node, cstruct, scale_validator)
        #     optional_validator('gravity', 'south_west', node, cstruct, string_validator)
        #     optional_validator('offset', '0,0', node, cstruct, string_validator)
        #     optional_validator('font-size', 10 , node, cstruct, number_validator)


class Layers(colander.SequenceSchema):
    layer = LayerSchemaNode()


class Coordinates(colander.SequenceSchema):
    coodinate = colander.SchemaNode(
        colander.Float()
    )


class ParamsSchemaNode(colander.MappingSchema):
    filename = colander.SchemaNode(
        colander.String(),
        missing='result',
        validator=colander.Length(4, 50)
    )
    epsg = colander.SchemaNode(
        colander.Integer(),
        validator=colander.OneOf([31370])
    )
    filetype = colander.SchemaNode(
        colander.String(),
        missing='png'
    )
    bbox = Coordinates(
        validator=colander.Length(4, 4)
    )
    width = colander.SchemaNode(
        colander.Integer()
    )
    height = colander.SchemaNode(
        colander.Integer()
    )

    def validator(self, node, cstruct):
        x1, y1, x2, y2 = cstruct['bbox']
        scale_image = float(cstruct['height'])/float(cstruct['width'])
        scale_bbox = float(y2-y1)/float(x2-x1)
        if scale_image < scale_bbox:
            x = (((y2-y1)/scale_image) - x2 + x1)/2
            cstruct['bbox'] = [x1 - x, y1, x2 + x, y2]
        elif scale_image > scale_bbox:
            y = ((scale_image * (x2-x1)) - y2 + y1)/2
            cstruct['bbox'] = [x1, y1 - y, x2, y2 + y]


class ConfigSchemaNode(colander.MappingSchema):
    params = ParamsSchemaNode()
    layers = Layers()
