# -*- coding: utf-8 -*-
"""OAuth / OpenID Connect authentication integration."""
from pyramid.authentication import SessionAuthenticationPolicy

from .oauth.scope import WEB_SCOPES


class OAuthPolicy(SessionAuthenticationPolicy):

    """
    Hybrid OAuth / session authentication.

    This authentication policy first checks the session authentication and
    then uses OAuth as a fallback. Afterward, the request will have attributes
    for ``client``, ``user`` and ``scope``. Any or all of them may be ``None``.
    """

    def unauthenticated_userid(self, request):
        if hasattr(request, 'user'):
            return request.user

        userid = super(OAuthPolicy, self).unauthenticated_userid(request)

        if userid is None:
            request.verify_request()
            request.client = getattr(request, 'client', None)
            request.user = getattr(request, 'user', None)
            request.scopes = getattr(request, 'scopes', None)
        else:
            request.client = request.registry.web_client
            request.user = userid
            request.scopes = WEB_SCOPES

        return request.user


def includeme(config):
    config.include('pyramid_oauthlib')
    authn_debug = config.registry.settings.get('debug_authorization')
    authn_policy = OAuthPolicy(debug=authn_debug, prefix='')
    config.set_authentication_policy(authn_policy)
