# -*- coding: utf-8 -*-
from mock import MagicMock
from pyramid import testing

from h.oauth import interfaces, lib


def test_get_client_ok():
    mock_consumer = MagicMock()
    settings = {'h.oauth.client_id': '1234'}
    with testing.testConfig(settings=settings) as config:
        registry = config.registry
        registry.registerUtility(mock_consumer, interfaces.IClientClass)
        request = testing.DummyRequest(registry=config.registry)
        lib.get_client(request, '4321')
        mock_consumer.fetch.assert_called_with('4321')


def test_get_client_not_ok():
    mock_consumer = MagicMock()
    mock_consumer.fetch.return_value = None
    settings = {'h.oauth.client_id': '1234'}
    with testing.testConfig(settings=settings) as config:
        registry = config.registry
        registry.registerUtility(mock_consumer, interfaces.IClientClass)
        request = testing.DummyRequest(registry=config.registry)
        assert lib.get_client(request, '9876') is None
