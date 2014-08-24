# -*- coding: utf-8 -*-
"""Library support for OAuth integration."""
from . import interfaces


try:
    # pylint: disable=no-name-in-module
    from hmac import compare_digest as is_equal
except ImportError:
    def is_equal(lhs, rhs):
        """Returns True if the two strings are equal, False otherwise.

        The comparison is based on a common implementation found in Django.
        This version avoids a short-circuit even for unequal lengths to reveal
        as little as possible. It takes time proportional to the length of its
        second argument.
        """
        result = 0 if len(lhs) == len(rhs) else 1
        lhs = lhs.ljust(len(rhs))
        for x, y in zip(lhs, rhs):
            result |= ord(x) ^ ord(y)
        return result == 0


def client_from_settings(config, prefix='h.oauth.'):
    """Get a :class:`h.oauth.IClientClass` implementation from settings."""
    registry = config.registry
    settings = registry.settings

    api_key = settings.get(prefix + 'client_id', 'annotate')
    api_secret = settings.get(prefix + 'client_secret')

    klass = registry.getUtility(interfaces.IClientClass)
    instance = klass.fetch(api_key)
    if instance is None:
        instance = klass(api_key, api_secret)
    else:
        if api_secret is not None and instance.client_secret != api_secret:
            msg = 'Setting "%ssecret" does not match stored secret.' % prefix
            raise RuntimeError(msg)

    return instance


def get_client(request, client_id):
    """Get a :class:`h.oauth.IClientClass` implementation from a client id."""
    registry = request.registry
    klass = registry.getUtility(interfaces.IClientClass)
    return klass.fetch(client_id)


def is_web_client(request, client_id):
    """True if the client id corresponds to the built-in Web client."""
    return client_id == request.registry.web_client.client_id
