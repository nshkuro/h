# -*- coding: utf-8 -*-
import os

from pyramid.interfaces import ISessionFactory
from pyramid.session import SignedCookieSessionFactory
from pyramid.view import view_config


def model(request):
    session = {k: v for k, v in request.session.items() if k[0] != '_'}
    session['csrf'] = request.session.get_csrf_token()
    return session


def pop_flash(request):
    session = request.session

    queues = {
        name[3:]: [msg for msg in session.pop_flash(name[3:])]
        for name in session.keys()
        if name.startswith('_f_')
    }

    # Deal with bag.web.pyramid.flash_msg style mesages
    for msg in queues.pop('', []):
        q = getattr(msg, 'kind', '')
        msg = getattr(msg, 'plain', msg)
        queues.setdefault(q, []).append(msg)

    return queues


def set_csrf_token(request, response):
    csrft = request.session.get_csrf_token()
    if request.cookies.get('XSRF-TOKEN') != csrft:
        response.set_cookie('XSRF-TOKEN', csrft)


@view_config(accept='application/json',  route_name='session', renderer='json')
@view_config(name='app', renderer='json')  # deprecated
def session(request):
    request.add_response_callback(set_csrf_token)
    return dict(status='okay', flash=pop_flash(request), model=model(request))


def session_from_config(settings, prefix='session.'):
    """Return a session factory from the provided settings."""
    secret_key = '{}secret'.format(prefix)
    secret = settings.get(secret_key)
    if secret is None:
        # Get 32 bytes (256 bits) from a secure source (urandom) as a secret.
        # Pyramid will add a salt to this. The salt and the secret together
        # will still be less than the, and therefore right zero-padded to,
        # 1024-bit block size of the default hash algorithm, sha512. However,
        # 256 bits of random should be more than enough for session secrets.
        secret = os.urandom(32)

    return SignedCookieSessionFactory(secret)


def includeme(config):
    def register():
        if config.registry.queryUtility(ISessionFactory) is None:
            session_factory = session_from_config(config.registry.settings)
            config.registry.registerUtility(session_factory, ISessionFactory)

    config.action(None, register, order=1)

    config.add_route('session', '/session')
    config.scan(__name__)
