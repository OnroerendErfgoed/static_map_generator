# -*- coding: utf-8 -*-
from pyramid.security import (
    Allow,
    Everyone
)

import logging
log = logging.getLogger(__name__)


class MapsFactory(object):
    __acl__ = [
        (Allow, Everyone, 'home'),
        (Allow, 'vioe-static-map-generator:beheerder', 'admin')
    ]


class RootFactory(object):
    __acl__ = [
        (Allow, Everyone, 'home'),
        (Allow, 'vioe-static-map-generator:beheerder', 'admin')
    ]

    _factories = {
        'maps': MapsFactory
    }

    def __init__(self, request):
        self.request = request

    def __getitem__(self, key):
        f = self._factories[key]
        f.__parent__ = self
        f.__name__ = str(key)
        return f
