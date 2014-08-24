# -*- coding: utf-8 -*-
from pyramid.testing import DummyRequest

from h.authentication import OAuthPolicy


def test_oauth_policy():
    def verify_request():
        request.client = 'sloth'
        request.user = 'wizard'
        request.scopes = ['paris']

    request = DummyRequest()
    request.session = {}

    request.verify_request = verify_request
    policy = OAuthPolicy(prefix='app.')
    userid = policy.unauthenticated_userid(request)

    assert request.client == 'sloth'
    assert request.user == userid == 'wizard'
    assert request.scopes == ['paris']


def test_oauth_policy_session_user():
    request = DummyRequest()
    request.registry.web_client = None
    request.session = {'app.userid': 'mbatu'}
    policy = OAuthPolicy(prefix='app.')
    assert policy.unauthenticated_userid(request) == 'mbatu'
