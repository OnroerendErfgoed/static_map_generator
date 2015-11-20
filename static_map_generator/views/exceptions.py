# -*- coding: utf-8 -*-
import sys

import logging

from pyramid.httpexceptions import HTTPBadRequest
from pyramid.view import notfound_view_config, view_config

log = logging.getLogger(__name__)


@notfound_view_config(renderer='json', accept='application/json')
def not_found(request):
    request.response.status_int = 404
    return {
        'message':
            'De door u gevraagde resource kon niet gevonden worden.'
    }


@view_config(context=KeyError, renderer='json')
def failed_no_result_found(exc, request):
    log.error(str(exc), exc_info=sys.exc_info())
    request.response.status_int = 404
    return {'message': 'De door u gevraagde resource kon niet gevonden worden.'}


# @view_config(context=ValueError, renderer='json', accept='application/json')
# def failed_validation(exc, request):
#     log.warn(exc.value)
#     log.warn(exc.errors)
#     request.response.status_int = 400
#     return {'value': exc.value, 'errors': exc.errors_info}

