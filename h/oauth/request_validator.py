# -*- coding: utf-8 -*-
"""OAuth request validation."""
from annotator import auth
from oauthlib import oauth2
from pyramid.exceptions import BadCSRFToken
from pyramid.session import check_csrf_token

from .lib import get_client, is_equal, is_web_client
from .scope import WEB_SCOPES


class RequestValidator(oauth2.RequestValidator):

    """
    A :class:`oauthlib.oauth2.RequestValidator` integration for h.

    This class utilizes the active :class:`h.interfaces.IClientClass` for
    authenticating clients. At this time, only client credentials and
    bearer tokens are supported. The client credentials can be implied by a
    valid authentication session.
    """

    def authenticate_client(self, request):
        if request.client_id is None and request.client_secret is None:
            try:
                check_csrf_token(request, token='assertion')
            except BadCSRFToken:
                return False
            client = request.registry.web_client
        else:
            client = get_client(request, request.client_id)

            if client is None:
                return False

            if not is_equal(client.client_secret, request.client_secret):
                return False

        request.client = client
        return True

    def get_default_scopes(self, client_id, request):
        if is_web_client(request, client_id):
            return WEB_SCOPES
        else:
            return []

    def save_bearer_token(self, token, request):
        # TODO: 3rd party authorizations
        # ------------------------------
        # Save authorizations so that they can be revoked so that access tokens
        # can be granted through non-interactive authorization flows, such as
        # refresh tokens and JWT bearer token grants.
        pass

    def validate_bearer_token(self, token, scopes, request):
        client = request.registry.web_client
        ttl = auth.DEFAULT_TTL
        try:
            token = auth.decode_token(token, client.client_secret, ttl)
        except auth.TokenInvalid:
            return False
        request.client = client  # TODO: 3rd party authorizations
        request.user = token.get('userId')
        request.scopes = token.get('scopes', [])
        return True

    def validate_grant_type(self, client_id, grant_type, client, request):
        return True

    def validate_scopes(self, client_id, scopes, client, request):
        if scopes is None:
            return True

        if is_web_client(request, client_id):
            return set(scopes) <= set(WEB_SCOPES)
        else:
            # TODO: 3rd party authorizations
            return set(scopes) <= set([])
