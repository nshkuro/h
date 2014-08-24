# -*- coding: utf-8 -*-
"""
Authentication and authorization

Authentication is handled by session authentication. Views can call the
``pyramid.security`` functions ``remember`` and ``forget``.

Authorization is handled by ``pyramid_oauthlib``.

Pyramid is not easily aligned with OAuth authorization. The reason for this is
that the :class:`pyramid.interfaces.IAuthorizationPolicy` APIs do not receive
the request object. As a result, this package provides an implementation of the
:class:`pyramid.interfaces.IAuthenticationPolicy` that executes the OAuth
machinery when the request is authenticated.

.. NOTE:: The current implementation provides limited support for OAuth, but
implements it nonetheless in order to plan for progressive enhancement with
more OAuth and OpenID connect framework features.

Supported grant types
---------------------

- The client credentials grant is the only grant type. It uses the provided
  ``client_id`` and ``client_secret`` request parameters. Otherwise, the Web
  client is assumed and it is authenticated using the session, with the
  cross-site request forgery token provided in the ``assertion`` parameter.

Supported token types
---------------------

- A bearer token implementation is provided by the :mod:`h.auth.tokens` module
  which generates Annotator-compatible access tokens.

Request validation
------------------

- An implementation of the ``RequestValidator`` class from
  :mod:`oauthlib.oauth2.request_validator` is provided that validates client
  credentials token requests and bearer token authorization to resource access.

Limitations
-----------

Almost no support for 3rd party applications exists yet. Applications can use
their client credentials, but they do not confer any authorizations and no
mechanism exists yet for users to grant authorizations to clients.
"""
from . import scope
from .interfaces import IClientClass
from .lib import client_from_settings
from .request_validator import RequestValidator
from .tokens import AnnotatorToken

__all__ = [
    'AnnotatorToken',
    'IClientClass',
    'RequestValidator',
    'client_from_settings',
    'scope',
]
