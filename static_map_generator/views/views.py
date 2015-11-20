# -*- coding: utf-8 -*-

import logging
log = logging.getLogger(__name__)

from pyramid.response import Response
from pyramid.view import view_config, view_defaults
from geozoekdiensten.search import (
    search_afbakeningen,
    search_admingrenzen
)
from geozoekdiensten.validators import (
    validate_afbakeningen_param_values,
    validate_admingrenzen_param_values
)
from geozoekdiensten.security import TableFactory
from pyramid.security import has_permission
from pyramid.httpexceptions import HTTPBadRequest
from pyramid_oeauth import get_system_token

import re


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
        if 'id' in self.request.matchdict and 'id' not in params:
            params['id'] = self.request.matchdict['id']
        return params

    def _get_valid_params(self, params, keys):
        p = dict()
        valid_keys = keys
        for k, v in params.items():
            if k in valid_keys:
                p[k] = v if k not in p else [p[k]] + [v]
        return p

    def parse_range_header(self, results):
        if 'Range' in self.request.headers:
            match = re.match('^items=([0-9]+)-([0-9]+)$', self.request.headers['Range'])
            if match:
                start = int(match.group(1))
                einde = int(match.group(2))
                einde = start if einde < start else einde
                einde = len(results) if len(results) < einde else einde
                start = einde if len(results) < start else start
                return results[start:einde] if len(results) != 0 else results
            else:
                return results
        else:
            return results

    def set_response_header(self, results_aantal, results_range_aantal):
        start = 0
        einde = start + results_range_aantal - 1 if results_range_aantal > 0 else 0
        self.request.response.headers['Content-Range'] = \
            'items %d-%d/%d' % (start, einde, results_aantal)

    @view_config(route_name='home', request_method='GET')
    def home(self):
        return Response(
            "Geozoekdienst: service voor het geografisch zoeken naar OE elementen en administratieve grenzen",
            content_type='text/plain', status_int=200)


@view_defaults(renderer='json', accept='application/json')
class AfbakeningenView(RestView):
    def __init__(self, request):
        super(AfbakeningenView, self).__init__(request)
        self.valid_keys = ['categorie', 'geometrie', 'buffer', 'geef_geometrie', 'type']

    def get_permitted_tables(self):
        tf = TableFactory(self.request)
        permitted_tables = [table for table in tf.table_store
                            if has_permission('view', tf[table.name], self.request)]
        return permitted_tables

    def _handle(self, params):
        search_parameters = self._get_valid_params(params, self.valid_keys)
        validated_search_params = validate_afbakeningen_param_values(search_parameters)
        tables = self.get_permitted_tables()
        results = search_afbakeningen(self.request, validated_search_params, tables)
        results_range = self.parse_range_header(results)
        self.set_response_header(len(results), len(results_range))
        self.request.response.status = '200'
        return results_range

    @view_config(route_name='afbakeningen', request_method='GET', permission='view')
    def afbakeningen_by_get(self):
        return self._handle(self.request.params)

    @view_config(route_name='afbakeningen', request_method='POST', permission='view')
    def afbakeningen_by_post(self):
        params = self._get_params()
        return self._handle(params)


@view_defaults(renderer='json', accept='application/json')
class AdmingrenzenView(RestView):
    def __init__(self, request):
        super(AdmingrenzenView, self).__init__(request)
        self.valid_keys = ['type', 'geometrie', 'buffer', 'geef_geometrie']
        self.admingrenzen_config = {
            'url': self.request.registry.settings['admingrenzen.url'],
            'layers': {
                'gemeente': self.request.registry.settings['admingrenzen.gemeente'],
                'provincie': self.request.registry.settings['admingrenzen.provincie'],
                'arrondissement': self.request.registry.settings['admingrenzen.arrondissement'],
                'gewest': self.request.registry.settings['admingrenzen.gewest']
            },
            'fields': {
                'geometrie': self.request.registry.settings['admingrenzen.geometry_field'],
                'naam': self.request.registry.settings['admingrenzen.name_field'],
                'niscode': self.request.registry.settings['admingrenzen.niscode_field']
            }
        }

    def _handle(self, params):
        search_parameters = self._get_valid_params(params, self.valid_keys)
        validated_search_params = validate_admingrenzen_param_values(search_parameters, self.admingrenzen_config['layers'])
        results = search_admingrenzen(self.request, validated_search_params, self.admingrenzen_config, get_system_token())
        results_range = self.parse_range_header(results)
        self.set_response_header(len(results), len(results_range))
        self.request.response.status = '200'
        return results_range

    @view_config(route_name='administratievegrenzen', request_method='GET', permission='view')
    def administratievegrenzen_by_get(self):
        return self._handle(self.request.params)

    @view_config(route_name='administratievegrenzen', request_method='POST', permission='view')
    def administratievegrenzen_by_post(self):
        params = self._get_params()
        return self._handle(params)
