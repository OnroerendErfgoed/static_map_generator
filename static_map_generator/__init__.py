# -*- coding: utf-8 -*-

from pyramid.config import Configurator
from pyramid.session import SignedCookieSessionFactory
from static_map_generator.renderer import json_item_renderer


def includeme(config):
    """
    Include `static_map_generator` in this `Pyramid` application.
    :param pyramid.config.Configurator config: A Pyramid configurator.
    """
    config.set_session_factory(SignedCookieSessionFactory(config.registry.settings['session_factory.secret']))

    # Rewrite urls with trailing slash
    config.include('pyramid_rewrite')
    config.add_rewrite_rule(r'/(?P<path>.*)/', r'/%(path)s')

    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('maps', '/maps', traverse='/maps')
    config.add_renderer('itemjson', json_item_renderer)

    # # Add authn/authz
    if config.registry.settings['oeauth.include'] == 'true':
        config.include('pyramid_oeauth')

    # Scanning the view package to load view_config objects
    config.scan('static_map_generator.views')


def main(global_config, **settings):
    """
    This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings, root_factory='static_map_generator.security.RootFactory')

    includeme(config)

    return config.make_wsgi_app()
