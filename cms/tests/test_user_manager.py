import unittest
import cms.user_management.manager as um
import cms.base_commands as bc
import krnch.wiring
from krnch.container import get_container
from krnch.routing import Bus
import krnch.secure as sec

_sample_user = {
    "email": "test@example.com",
    "password": "Chavez21@",
    "client_id": "TPPYEAJGHm8t4mrjn36wLYqCQRb"
}


class TestUserAddCommand(unittest.TestCase):
    """ Test cases for user management. """
    def setUp(self):
        self.sample_user = dict(_sample_user)
        self.ctr = get_container()
        self.bus = self.ctr.get(Bus)

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
            self.sample_user["email"] = "wrongwrong"
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

class TestUserManager(unittest.TestCase):
    """ Tests the user manager class. """
    def setUp(self):
        self.ctr = get_container()
        self.bus = self.ctr.get(Bus)
        self.sample_user = dict(_sample_user)

    def tearDown(self):
        pass

    def test_add_user(self):
        cmd = um.UserAddCommand(self.sample_user)
        response = self.bus.dispatch(cmd)
        self.assertTrue(response.result_code == bc.SUCCESS)
        self.assertTrue(response.result)
        #self.assertTrue(response.result["email"] == self.sample_user["email"])
        # self.assertTrue(sec.verify_password(self.sample_user["password"], response.result["password_hash"]))

    def test_user_login(self):
        login = {"email": "bob@example.com", "password": "xxxxx"}
        cmd = um.UserLoginCommand(login)
        self.bus.dispatch(cmd)


if __name__ == "__main__":
    unittest.main()
