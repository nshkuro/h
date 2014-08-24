# -*- coding: utf-8 -*-
import base64
import os
import re

from hem.interfaces import IDBSession
from hem.db import get_session
from horus.interfaces import (
    IActivationClass,
    IUserClass,
    IUIStrings,
)
from horus.models import (
    BaseModel,
    ActivationMixin,
    GroupMixin,
    UserMixin,
    UserGroupMixin,
)
from horus.strings import UIStringsBase
from pyramid_basemodel import Base, Session
from pyramid.threadlocal import get_current_request
from sqlalchemy import event, func, or_
from sqlalchemy.schema import Column
from sqlalchemy.types import String
import transaction
from zope.interface import implementer

from h.oauth import IClientClass, client_from_settings


class Activation(ActivationMixin, Base):
    def __init__(self, *args, **kwargs):
        super(Activation, self).__init__(*args, **kwargs)

        # XXX: Horus currently has a bug where the Activation model isn't
        # flushed before the email is generated, causing the link to be
        # broken (hypothesis/h#1156).
        #
        # Fixed in horus@90f838cef12be249a9e9deb5f38b37151649e801
        request = get_current_request()
        db = get_session(request)
        db.add(self)
        db.flush()


@implementer(IClientClass)
class ClientMixin(BaseModel):

    """
    OAuth client credential storage.

    The API uses this class for authenticating requests.
    """

    client_id = Column(String, index=True, nullable=False)
    client_secret = Column(String, nullable=False)

    def __init__(self, client_id, client_secret=None):
        self.client_id = client_id
        self.client_secret = client_secret or \
            base64.urlsafe_b64encode(os.urandom(18))

    def __repr__(self):
        return '<Client %r>' % self.client_id

    @classmethod
    def fetch(cls, client_id):
        return Session().query(cls).filter(cls.client_id == client_id).first()


class Client(ClientMixin, Base):
    pass


class Group(GroupMixin, Base):
    pass


class User(UserMixin, Base):

    @classmethod
    def get_by_id(cls, request, userid):
        match = re.match(r'acct:([^@]+)@{}'.format(request.domain), userid)
        if match:
            return cls.get_by_username(request, match.group(1))
        else:
            return super(User, cls).get_by_id(request, userid)

    @classmethod
    def get_by_username(cls, request, username):
        session = get_session(request)

        lhs = func.replace(cls.username, '.', '')
        rhs = username.replace('.', '')
        return session.query(cls).filter(
            func.lower(lhs) == rhs.lower()
        ).first()

    @classmethod
    def get_by_username_or_email(cls, request, username, email):
        session = get_session(request)

        lhs = func.replace(cls.username, '.', '')
        rhs = username.replace('.', '')
        return session.query(cls).filter(
            or_(
                func.lower(lhs) == rhs.lower(),
                cls.email == email
            )
        ).first()

    @property
    def email_confirmed(self):
        return bool((self.status or 0) & 0b001)

    @email_confirmed.setter
    def email_confirmed(self, value):
        if value:
            self.status = (self.status or 0) | 0b001
        else:
            self.status = (self.status or 0) & ~0b001

    @property
    def optout(self):
        return bool((self.status or 0) & 0b010)

    @optout.setter
    def optout(self, value):
        if value:
            self.status = (self.status or 0) | 0b010
        else:
            self.status = (self.status or 0) & ~0b010

    @property
    def subscriptions(self):
        return bool((self.status or 0) & 0b100)

    @subscriptions.setter
    def subscriptions(self, value):
        if value:
            self.status = (self.status or 0) | 0b100
        else:
            self.status = (self.status or 0) & ~0b100


class UserGroup(UserGroupMixin, Base):
    pass


def create_event_listeners(config):
    # The sqlalchemy table object is created magically at runtime
    table = Client.__table__  # pylint: disable=no-member

    @event.listens_for(table, 'after_create')
    def create_api_client(target, connection, **kwargs):
        client = client_from_settings(config)
        with transaction.manager:
            session = Session()
            session.add(client)
            session.flush()


def includeme(config):
    registry = config.registry

    models = [
        (IActivationClass, Activation),
        (IUserClass, User),
        (IUIStrings, UIStringsBase),
        (IClientClass, Client),
        (IDBSession, Session),
    ]

    for iface, imp in models:
        if not registry.queryUtility(iface):
            registry.registerUtility(imp, iface)

    create_event_listeners(config)
