# -*- coding: utf-8 -*-
import sys
from sqlalchemy.orm.exc import NoResultFound

from pyramid.view import (
    view_config,
    notfound_view_config)

import logging
from geozoekdiensten.validators import ValidationError

log = logging.getLogger(__name__)


@notfound_view_config(renderer='json', accept='application/json')
def not_found(request):
    request.response.status_int = 404
    return {
        'message':
            'De door u gevraagde resource kon niet gevonden worden.'
    }

@view_config(context=NoResultFound, renderer='json')
def failed_no_result_found(exc, request):
    log.error(str(exc), exc_info=sys.exc_info())
    request.response.status_int = 404
    return {'message': 'De door u gevraagde resource kon niet gevonden worden.'}


@view_config(context=ValidationError, renderer='json', accept='application/json')
def failed_validation(exc, request):
    log.warn(exc.value)
    log.warn(exc.errors)
    request.response.status_int = 400
    return {'value': exc.value, 'errors': exc.errors_info}

@view_config(context=Exception, renderer='json', accept='application/json')
def internal_server_error(exc, request):
    log.error(str(exc), exc_info=sys.exc_info())
    request.response.status_int = 500
    return {'message': 'Er ging iets fout in de server. Onze excuses.'}

