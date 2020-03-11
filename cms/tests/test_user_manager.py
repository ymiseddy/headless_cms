import unittest

from krnch.db import Provider
from krnch.tools import new_id

import cms.user_management.manager as um
import cms.base_commands as bc
from krnch.container import get_container
import krnch.eventstore as es
from krnch.eventstore.memory_eventstorageengine import MemoryEventStorageEngine
from cms.tests.setup import sample_user
from cms.tools import PropertyBag


class MockUserRepository:
    def __init__(self):
        self.users = []

    def add_user(self, user):
        duplicate = any([u.email == email or u.entity_id == entity_id for u in self.users])

        if duplicate:
            raise Exception("User already exists")
        u = PropertyBag(user.__dict__)
        self.users.append(u)

    def update_user(self, entity_id, email, first_name, last_name):
        u = [user for user in self.users if user.entity_id == entity_id][0]
        u.email = email
        u.first_name = first_name
        u.last_name = last_name

    def get_user_by_entity_id(self, entity_id):
        u = [user for user in self.users if user.entity_id == entity_id]
        if not u:
            return None
        return u[0]

    def get_user_by_email(self, email):
        u = [user for user in self.users if user.email == email]
        if not u:
            return None
        return u[0]


class TestUserManager(unittest.TestCase):
    """ Tests the user manager class. """

    def setUp(self):
        self.ctr = get_container()

        connections = {"main": {"type": "mock"}}
        provider = Provider(connections)
        self.storage_engine = MemoryEventStorageEngine(provider)
        self.es = es.EventStore(self.storage_engine)
        self.sample_user = PropertyBag(sample_user)
        self.repository = MockUserRepository()
        self.manager = um.UserManager(self.es, self.repository)

    def tearDown(self):
        pass

    def _add_sample_user(self):
        cmd = um.UserAddCommand(self.sample_user)
        response = self.manager.handle_user_add(cmd)
        return response

    def test_add_user(self):
        response = self._add_sample_user()

        self.assertTrue(response.result_code == bc.SUCCESS)
        self.assertTrue(response.result)

    def test_add_user_fails_if_user_exists(self):
        self._add_user_to_repository()

        response = self._add_sample_user()

        self.assertTrue(response.result_code == bc.ERR_DUPLICATE)

    def test_user_login(self):
        cmd = um.UserLoginCommand({"email": self.sample_user.email, "password": self.sample_user.password})

    def test_user_sign_in(self):
        user_id = self._add_sample_user().result
        self._add_user_to_repository(user_id)
        login = {
            "email": self.sample_user.email,
            "password": self.sample_user.password
        }
        cmd = um.UserLoginCommand(login)

        response = self.manager.handle_user_login(cmd)

        self.assertEqual(response.result_code, bc.SUCCESS)
        event = self.storage_engine.events[1]
        self.assertEqual(event["event"].event_name, um.User.EVT_SIGNED_IN)

    def test_user_sign_in_invalid_password(self):
        user_id = self._add_sample_user().result
        self._add_user_to_repository(user_id)
        login = {
            "email": self.sample_user.email,
            "password": "wrong"
        }
        cmd = um.UserLoginCommand(login)

        response = self.manager.handle_user_login(cmd)

        self.assertEqual(response.result_code, bc.ERR_AUTHENTICATION_FAILED)
        event = self.storage_engine.events[1]
        self.assertEqual(event["event"].event_name, um.User.EVT_SIGN_IN_FAILED)

    def test_user_sign_in_does_not_exist(self):
        user_id = self._add_sample_user().result
        login = {
            "email": self.sample_user.email,
            "password": "wrong"
        }
        cmd = um.UserLoginCommand(login)

        response = self.manager.handle_user_login(cmd)

        self.assertEqual(response.result_code, bc.ERR_AUTHENTICATION_FAILED)

    def test_user_sign_in_missing_from_eventstore(self):
        self._add_user_to_repository()
        login = {
            "email": self.sample_user.email,
            "password": "wrong"
        }
        cmd = um.UserLoginCommand(login)

        response = self.manager.handle_user_login(cmd)

        self.assertEqual(response.result_code, bc.ERR_AUTHENTICATION_FAILED)

    def _add_user_to_repository(self, user_id=None):
        if user_id:
            self.sample_user.entity_id = user_id
        else:
            self.sample_user.entity_id = new_id()
        self.repository.add_user(self.sample_user)
        del self.sample_user["entity_id"]


if __name__ == "__main__":
    unittest.main()
