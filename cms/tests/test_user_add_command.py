import unittest

from cms import base_commands as bc
from cms.tests.setup import sample_user
from cms.tools import PropertyBag
from cms.user_management import manager as um


class TestUserAddCommand(unittest.TestCase):
    """ Test cases for user management. """

    def setUp(self):
        self.sample_user = PropertyBag(sample_user)

    def tearDown(self):
        pass

    def test_create_user_requires_email(self):
        """ Ensures creating a user requires an email address. """
        with self.assertRaises(bc.ValidationError) as ctx:
            del self.sample_user["email"]
            um.UserAddCommand(self.sample_user)
        self.assertTrue("email" in ctx.exception.errors)

    def test_create_user_requires_a_valid_email(self):
        """ Ensures creating a user requires an email address. """
        with self.assertRaises(bc.ValidationError) as ctx:
            self.sample_user.email = "wrongwrong"
            um.UserAddCommand(self.sample_user)
        self.assertTrue("email" in ctx.exception.errors)

    def test_create_user_requires_password(self):
        """ Ensures creating a user requires a password. """
        with self.assertRaises(bc.ValidationError) as ctx:
            del self.sample_user["password"]
            um.UserAddCommand(self.sample_user)
        self.assertTrue("password" in ctx.exception.errors)

    def test_create_user_password_must_contain_lowercase(self):
        """ Checking password requirmenets """
        with self.assertRaises(bc.ValidationError) as ctx:
            self.sample_user["password"] = "CHAVEZ21@"
            um.UserAddCommand(self.sample_user)
        self.assertTrue("password" in ctx.exception.errors)

    def test_create_user_password_must_contain_uppercase(self):
        """ Checking password requirmenets """
        with self.assertRaises(bc.ValidationError) as ctx:
            self.sample_user["password"] = "chavez21@"
            um.UserAddCommand(self.sample_user)
        self.assertTrue("password" in ctx.exception.errors)

    def test_create_user_password_must_contain_number(self):
        """ Checking password requirmenets """
        with self.assertRaises(bc.ValidationError) as ctx:
            self.sample_user["password"] = "Chavez@@@"
            um.UserAddCommand(self.sample_user)
        self.assertTrue("password" in ctx.exception.errors)

    def test_create_user_password_must_contain_a_symbol(self):
        """ Checking password requirmenets """
        with self.assertRaises(bc.ValidationError) as ctx:
            self.sample_user["password"] = "Chavez222"
            um.UserAddCommand(self.sample_user)
        self.assertTrue("password" in ctx.exception.errors)

    def test_create_user_password_is_a_minimum_length_of_eight(self):
        """ Checking password requirmenets """
        with self.assertRaises(bc.ValidationError) as ctx:
            self.sample_user["password"] = "Czzz@22"
            um.UserAddCommand(self.sample_user)
        self.assertTrue("password" in ctx.exception.errors)

    def test_create_user_allows_missing_client(self):
        """ Client id's nore not strictly required. """
        del self.sample_user["client_id"]
        um.UserAddCommand(self.sample_user)

    def test_create_user_allows_client_id_is_base58check(self):
        """ Client id's should be base58check formatted ids """
        with self.assertRaises(bc.ValidationError) as ctx:
            self.sample_user["client_id"] = "invalid"
            um.UserAddCommand(self.sample_user)
        self.assertTrue("client_id" in ctx.exception.errors)