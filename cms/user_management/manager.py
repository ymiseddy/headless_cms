""" User Management """
from krnch.container import provides

import cms.base_commands as bc
import krnch.routing as kr
import krnch.tools as kt
import krnch.eventstore as es
import krnch.secure as sec
from krnch.db import Provider

from cms.tools import check_base58, check_valid_password, PropertyBag


# ========================== COMMANDS ==============================

class UserAddCommand(bc.ValidatingCommand):
    """ Command that adds a new article. """
    schema = {
        "email": {"type": "string", "required": True,
                  "regex": r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"},
        "password": {"type": "string", "required": True, "check_with": check_valid_password},
        "first_name": {"type": "string", "required": True, "minlength": 2, "maxlength": 20},
        "last_name": {"type": "string", "required": True, "minlength": 2, "maxlength": 20},
    }


# ========================== QUERIES  ==============================

class UserGetQuery(bc.ValidatingCommand):
    """ Retrieve a user """
    schema = {
        "id": {"type": "string", "check_with": check_base58},
        "email": {"type": "string"}
    }


class User(es.DataEntity):
    """ User entity """
    EVT_SIGNED_IN = "signed_in"
    EVT_SIGN_IN_FAILED = "sign_in_failed"

    entity_type = "Uwer"
    email = es.attribute()
    first_name = es.attribute()
    last_name = es.attribute()
    password_hash = es.attribute()
    must_change_password = es.attribute()

    def sign_in(self, password):
        if not sec.verify_password(password, self.password_hash):
            event = es.Event(self.EVT_SIGN_IN_FAILED, self.entity_type, self.entity_id, self.version + 1, {})
            self.publisher.publish(self, event)
            return False

        event = es.Event(self.EVT_SIGNED_IN, self.entity_type, self.entity_id, self.version + 1, {})
        self.publisher.publish(self, event)
        return True

    def _handle_signed_in(self, event):
        """ Not doing anything at the moment here. """
        pass

    def _handle_sign_in_failed(self, event):
        """ Not doing anything at the moment here. """
        pass

class UserLoginCommand(bc.ValidatingCommand):
    """ User logs in """
    schema = {
        "email": {"type": "string", "required": True},
        "password": {"type": "string", "required": True}
    }


@provides()
class UserRepository:
    def __init__(self, provider: Provider, connection_name="main"):
        self.provider = provider
        self.connection_name = connection_name

    def add_user(self, user_info: dict):
        dataset = dict((k, user_info[k]) for k in ["email", "first_name", "last_name", "entity_id"])
        with self.provider.get_open_connection(self.connection_name) as conn:
            conn.insert(dataset)

    def update_user(self, user_info):
        with self.provider.get_open_connection(self.connection_name) as conn:
            updates = dict((k, user_info[k]) for k in ["email", "first_name", "last_name"])
            conn.update("users", updates, {"entity_id": user_info["entity_id"]})

    def get_user_by_email(self, email):
        with self.provider.get_open_connection(self.conneciton_name) as conn:
            results = conn.select("users", {"email": email}, {"entity_id", "email", "first_name", "last_name"})
        if results:
            return PropertyBag(results[0])
        return None

"""
class UserService:
    def __init__(self, provider: Provider, repository: UserRepository, eventstore: es.EventStore):
        self.repository = repository
        self.provider = provider
        self.eventstore = eventstore
        self.eventstore.subscribe("user", self._user_events)

    def _user_events(self, user_entity: User, event: es.Event):
        if es.Event.event_name == "created":

            pass
        if es.Event.event_name == "updated":
            pass
"""


@kr.service
class UserManager:
    """ Handles user managemnt commands."""

    def __init__(self, eventstore: es.EventStore, repository: UserRepository):
        self.eventstore = eventstore
        self.repository = repository

    @kr.handles(UserAddCommand)
    def handle_user_add(self, cmd: UserAddCommand):
        """ Handles adding a new user. """

        # TODO: Ensure email is not already used.
        existing = self.repository.get_user_by_email(cmd.email)
        if existing:
            return bc.DispatchResponse(bc.ERR_DUPLICATE)

        with self.eventstore.context() as ctx:
            user = ctx.new(User, kt.new_id())
            cmd.map(user, drop=("client_id", ))
            user.password_hash = sec.hash_password(cmd.password)
            user.save()
            user_id = user.entity_id
        return bc.DispatchResponse(bc.SUCCESS, user_id)

    @kr.handles(UserLoginCommand)
    def handle_user_login(self, cmd):
        """ Handles user login """
        user_rec = self.repository.get_user_by_email(cmd.email)
        if user_rec is None:
            return bc.DispatchResponse(bc.ERR_AUTHENTICATION_FAILED)

        with self.eventstore.context() as ctx:
            user = ctx.load(User, user_rec.entity_id)

            if user is None:
                return bc.DispatchResponse(bc.ERR_AUTHENTICATION_FAILED)

            result = user.sign_in(cmd.password)
            if result:
                return bc.DispatchResponse(bc.SUCCESS, user.entity_id)
            else:
                return bc.DispatchResponse(bc.ERR_AUTHENTICATION_FAILED)
