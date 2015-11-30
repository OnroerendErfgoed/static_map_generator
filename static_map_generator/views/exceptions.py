# -*- coding: utf-8 -*-
import sys

import logging

from pyramid.httpexceptions import HTTPBadRequest
from pyramid.view import notfound_view_config, view_config
from static_map_generator.validators import ValidationFailure

log = logging.getLogger(__name__)


@notfound_view_config(renderer='json', accept='application/json')
def not_found(request):
    request.response.status_int = 404
    return {
        'message':
            'De door u gevraagde resource kon niet gevonden worden.'
    }


@view_config(
    context=ValidationFailure,
    renderer='json'
)
def failed_validation(exc, request):
    log.debug(exc.msg)
    log.debug(exc.errors)
    request.response.status_int = 400
    formated_errors = [' '.join(list(reversed(node.split('.')))).capitalize() + ': ' + exc.errors[node]
                       for node in exc.errors]
    return {'message': exc.msg, 'errors': formated_errors}

