import cms.base_commands as bc
import base58
import krnch.routing as kr
import krnch.tools as kt
import krnch.eventstore as es
import krnch.secure as sec

def check_base58(field, value, error):
    try:
        decoded_bytes = base58.b58decode_check(value)
    except ValueError:
        error(field, "Must be a valid id.")

def check_valid_password(field, value, error):
    if len(value) < 8:
        error(field, "Passwords must be at least eight characters.")
    msg = "Passwords must contain at least one upper case letter, one lowercase" + \
          " letter, one digit and one symbol."
    if not any([c.islower() for c in value]):
        error(field, msg)
    if not any([c.isupper() for c in value]):
        error(field, msg)
    if not any([c.isdigit() for c in value]):
        error(field, msg)
    if not any([c.isdigit() for c in value]):
        error(field, msg)
    if not any([not c.isalnum() for c in value]):
        error(field, msg)

class UserAddCommand(bc.ValidatingCommand):
    """ Command that adds a new article. """
    schema = {
        "email": {"type": "string", "required": True,
                  "regex": r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"},
        "password": {"type": "string", "required": True, "check_with": check_valid_password},
        "client_id": {"type": "string", "check_with": check_base58},
    }

class UserGetQuery(bc.ValidatingCommand):
    """ Retrieve a user """
    schema = {
        "id": {"type": "string", "check_with": check_base58}
    }

class User(es.DataEntity):
    """ User entity """
    email = es.attribute()
    password_hash = es.attribute()
    must_change_password = es.attribute


@kr.service
class UserManager:

    def __init__(self, eventstore: es.EventStore):
        self.eventstore = eventstore

    @kr.handles(UserAddCommand)
    def handle_user_add(self, cmd):
        """ Handles adding a new user. """

        # TODO: Ensure email is not already used.
        with self.eventstore.context() as ctx:
            user = ctx.new(User, kt.new_id())
            cmd.map(user)
            user.password_hash = sec.hash_password(cmd.password)
            user.save()
            state = user.state
            return bc.DispatchResponse(bc.SUCCESS, state)

    @kr.handles(UserLoginCommand)
    def handle_user_login(self, cmd):
        """ Handles user login> """
        pass
