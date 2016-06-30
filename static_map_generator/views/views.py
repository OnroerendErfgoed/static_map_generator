# -*- coding: utf-8 -*-

import logging

from static_map_generator.generator import Generator
from pyramid.response import Response
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPBadRequest
import colander
from static_map_generator.validators import ValidationFailure

log = logging.getLogger(__name__)


class RestView(object):
    def __init__(self, request):
        self.request = request

    def _get_params(self):
        try:
            params = self.request.json_body
        except AttributeError as e:
            raise HTTPBadRequest(detail="Request bevat geen json body. \n%s" % e)
        except ValueError as e:
            raise HTTPBadRequest(detail="Request bevat incorrecte json body. \n%s" % e)
        return params

    @staticmethod
    def validate_config(params):
        from static_map_generator.validators import (
            ConfigSchemaNode as config_schema
        )
        try:
            return config_schema().deserialize(params)
        except colander.Invalid as e:
            raise ValidationFailure(
                'De configuratie is niet geldig.',
                e.asdict()
            )

    @view_config(route_name='home', request_method='GET', permission='home')
    def home(self):
        return Response(
            "Static_map_generator: service voor het genereren van een statische kaart op basis van verschillende "
            "geografische databronnen (wms, wkt, geojson,...)",
            content_type='text/plain', status_int=200)

    @view_config(route_name='maps', request_method='POST', accept='application/octet-stream', permission='admin')
    def maps_by_post_stream(self):
        params = self._get_params()
        config = self.validate_config(params)
        res = Response(content_type='image/png')
        res.status = '200 OK'
        res.body = Generator.generate_stream(config)
        return res

    @view_config(route_name='maps', request_method='POST', accept='application/json', renderer='itemjson', permission='admin')
    def maps_by_post_base64(self):
        params = self._get_params()
        config = self.validate_config(params)
        self.request.response.status = 201
        return {
            'image':  Generator.generate_base64(config)
        }



