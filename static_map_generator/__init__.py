# -*- coding: utf-8 -*-

from pyramid.config import Configurator
from pyramid.session import SignedCookieSessionFactory


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings, root_factory='static_map_generator.security.RootFactory')
    config.set_session_factory(SignedCookieSessionFactory(config.registry.settings['session_factory.secret']))

    # Rewrite urls with trailing slash
    config.include('pyramid_rewrite')
    config.add_rewrite_rule(r'/(?P<path>.*)/', r'/%(path)s')

    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('maps', '/maps', traverse='/maps')

    # Add authn/authz
    config.include('pyramid_oeauth')

    config.scan()
    return config.make_wsgi_app()
