# -*- coding: utf-8 -*-
import sys

import logging

from pyramid.security import authenticated_userid
from pyramid.view import notfound_view_config, view_config, forbidden_view_config
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


@view_config(context=Exception, renderer='json', accept='application/json')
def internal_server_error(exc, request):
    log.error(str(exc), exc_info=sys.exc_info())
    request.response.status_int = 500
    return {'message': 'Er ging iets fout in de server. Onze excuses.'}


@forbidden_view_config(accept='application/json', renderer='json')
def forbidden_view(exc, request):
    log.debug('FORBIDDEN anything')
    log.debug(exc)
    log.debug(exc.message)
    log.debug(exc.result)
    err = {
        'message': 'U bent niet gemachtigd om deze actie uit te voeren.',
        'errors': []
    }
    request.response.status_int = 401
    return err

