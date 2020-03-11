import base58


class PropertyBag(dict):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__dict__ = self


def automap(struct: dict, instance: object, keep: iter = None, drop: iter = None):
    """ Maps a dictionary into an objects properties. """
    items = struct.items()

    # Keep only the specified keys
    if keep is not None:
        items = [(k, v) for (k, v) in items if k in keep]

    # Drop the specified keys
    if drop is not None:
        items = [(k, v) for (k, v) in items if k not in drop]

    for key, value in items:
        if hasattr(instance, key):
            setattr(instance, key, value)


def check_base58(field, value, error):
    """ Ensure value is a valid base58check id. """
    try:
        decoded_bytes = base58.b58decode_check(value)
    except ValueError:
        error(field, "Must be a valid id.")


def check_valid_password(field, value, error):
    """ Checks to ensure value follows password conventions. """
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
