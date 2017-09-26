# -*- coding: utf-8 -*-
import colander
import rfc3987
from shapely import geometry
import json
import geojson
from pyramid.compat import text_, long


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
    try:
        value = text_(value)
    except:
        raise colander.Invalid(
            node,
            u"{} is not a valid string".format(value)
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


def gravity_validator(node, value):
    """
    Gravity validator

    :param node: The schema node to which this exception relates.
    :param value: Value to validate.
    """
    if value not in ['center', 'north_west', 'north_east', 'south_west', 'south_east']:
        raise colander.Invalid(
            node,
            "{} is not one of the following gravities: 'center', 'north_west', 'north_east', 'south_west', "
            "'south_east'".format(value)
        )


def required_validator(param, type, node, cstruct, validator=None):
    """
    Param is required in cstruct for type in node.
    Validates the param with validator (if provided).

    :param param: Required param.
    :param type: The layer type (wms', 'geojson', 'text').
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
            validator=colander.OneOf(['wms', 'geojson', 'text'])
    )

    def validator(self, node, cstruct):
        if cstruct['type'] == 'wms':
            required_validator('url', 'wms', node, cstruct, uri_validator)
            required_validator('layers', 'wms', node, cstruct, string_validator)
        elif cstruct['type'] == 'geojson':
            required_validator('geojson', 'geojson', node, cstruct, geojson_validator)
            optional_validator('color', 'steelblue', node, cstruct, string_validator)
        elif cstruct['type'] == 'text':
            required_validator('text', 'text', node, cstruct, string_validator)
            required_validator('gravity', 'center', node, cstruct, gravity_validator)
            required_validator('font_size', 10, node, cstruct, number_validator)


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
    bbox = Coordinates(
        validator=colander.Length(4, 4),
        missing=None
    )
    width = colander.SchemaNode(
        colander.Integer()
    )
    height = colander.SchemaNode(
        colander.Integer()
    )


class ConfigSchemaNode(colander.MappingSchema):
    params = ParamsSchemaNode()
    layers = Layers()
