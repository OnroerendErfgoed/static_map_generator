# -*- coding: utf-8 -*-

import logging

from static_map_generator.generator import Generator
from pyramid.response import Response
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPBadRequest

log = logging.getLogger(__name__)


class RestView(object):
    def __init__(self, request):
        self.request = request

    def _get_params(self):
        try:
            params = self.request.json_body
        except AttributeError as e:
            raise HTTPBadRequest(detail="Request bevat geen json body. \n%s" % e)
        return params

    @view_config(route_name='home', request_method='GET')
    def home(self):
        return Response(
            "Static_map_generator: service voor het genereren van een statische kaart op basis van verschillende geografische databronnen (wms, wkt, geojson,...)",
            content_type='text/plain', status_int=200)

    @view_config(route_name='maps', request_method='POST', accept='application/json')
    def maps_by_post(self):
        config = self._get_params()
        res = Response(content_type='image/png')
        res.status = '200 OK'
        res.body = Generator.generateStream(config)
        return res



