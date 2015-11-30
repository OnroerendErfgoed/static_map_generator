# -*- coding: utf-8 -*-
import colander
import rfc3987
from shapely import wkt, geometry
import json
import geojson


def uri_validator(node, uri):
    """ URL validator. rfc3987 is used to check if a URL is correct (https://pypi.python.org/pypi/rfc3987/)
    If ``msg`` is supplied, it will be the error message to be used when raising :exc:`colander.Invalid`;
    otherwise, defaults to 'Invalid URL'.
    """
    if not rfc3987.match(uri, rule='URI'):
        raise colander.Invalid(node, '{0} is geen geldige URI.'.format(uri))


def wkt_validator(node, wkt_input):
    """
    Try to parse wkt with Shapely
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
    Try to parse geojson with geojson and shapely
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
    Check if string
    """
    if not isinstance(value, (str, unicode)) or len(value) == 0:
        raise colander.Invalid(
            node,
            "{} is not a valid sting".format(value)
        )


def check_required(param, type, node, cstruct):
    if param not in cstruct:
        raise colander.Invalid(
            node,
            "{0} is required for {1} configuration".format(param, type)
        )


def check_optional(param, default, cstruct):
        return cstruct[param] if param in cstruct else default


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
            check_required('url', 'wms', node, cstruct)
            uri_validator(node, cstruct['url'])
            check_required('layers', 'wms', node, cstruct)
            string_validator(node, cstruct['layers'])
        elif cstruct['type'] == 'wkt':
            check_required('wkt', 'wkt', node, cstruct)
            wkt_validator(node, cstruct['wkt'])
            cstruct['color'] = check_optional('color', 'steelblue', cstruct)
            cstruct['opacity'] = check_optional('opacity', 0.5, cstruct)
        elif cstruct['type'] == 'geojson':
            geojson_validator(node, cstruct['geojson'])
            cstruct['color'] = check_optional('color', 'steelblue', cstruct)
            cstruct['opacity'] = check_optional('opacity', 0.5, cstruct)


class Layers(colander.SequenceSchema):
    layer = LayerSchemaNode()


class ParamsSchemaNode(colander.MappingSchema):
    filename = colander.SchemaNode(
        colander.String(),
        validator=colander.Length(4, 50)
    )
    epsg = colander.SchemaNode(
        colander.Integer()
    )
    filetype = colander.SchemaNode(
        colander.String(),
        missing='png'
    )
    bbox = colander.SchemaNode(
        colander.List(),
        validator=colander.Length(4, 4)
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
