# -*- coding: utf-8 -*-
"""OAuth authorization integration.

.. NOTE:: There is no provided capability for securing contexts or views using
the OAuth scopes yet.
"""
from oauthlib.oauth2 import ClientCredentialsGrant
from pyramid.authorization import ACLAuthorizationPolicy

from .oauth import AnnotatorToken, RequestValidator


def includeme(config):
    config.include('pyramid_oauthlib')

    request_validator = RequestValidator()
    config.add_grant_type(ClientCredentialsGrant, 'client_credentials',
                          request_validator=request_validator)
    config.add_token_type(AnnotatorToken, request_validator=request_validator)

    # Configure the authorization policy
    authz_policy = ACLAuthorizationPolicy()
    config.set_authorization_policy(authz_policy)
