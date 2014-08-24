# -*- coding: utf-8 -*-
from zope.interface import Attribute, Interface


class IClientClass(Interface):

    """Classes implementing this interface represent an OAuth client."""

    client_id = Attribute(
        """
        A unique identifier for this client.

        The identifier should be a URL-safe base64 encoded string.
        """
    )

    client_secret = Attribute(
        """
        A signing secret for client authentication.

        The secret should be a URL-safe base64 encoded string.
        """
    )

    def __init__(client_id, client_secret=None):  # noqa
        """Initialize a consumer with a ``client_id`` and ``client_secret``.

        If not provided, the ``client_secret`` should be set to a secure,
        random secret so that single-server deployment is easy out of the box.
        """

    def fetch(client_id):  # noqa
        """Fetch a consumer from storage given a ``client_id``.

        Returns ``None`` if the consumer does not exist or the implementation
        does not support persistence.

        ..Note:: this should be implemented as a class method.
        """
