import cerberus
import json

from cms.tools import automap

SUCCESS = 0
ERR_AUTHENTICATION_FAILED = 401
ERR_NOT_FOUND = 404
ERR_DUPLICATE = 409
ERR_SYSTEM_ERROR = 500


class ValidationError(Exception):
    """ Error in validation. """

    def __init__(self, message, errors):
        super().__init__(message)
        self.errors = errors


class DispatchResponse:
    """ Response that handlers ought to return """

    def __init__(self, result_code, result=None, message=None):
        self.result_code = result_code
        self.result = result
        self.message = message


class ValidatingCommand:
    """ Base command that validates a struct and raises on errors. """

    def __init__(self, struct: dict):
        if isinstance(struct, str):
            struct = json.loads(struct)
        validator = cerberus.Validator(self.schema, purge_unknown=True)
        result = validator.validate(struct)
        if not result:
            raise ValidationError("Please correct these errors", validator.errors)

        self.struct = validator.document

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if not hasattr(cls, 'schema'):
            raise TypeError("ValidatingCommand requires a class level schema.")

    def map(self, instance, keep=None, drop=None):
        """ Maps the contents of the command's struct into matching attributes of instance """
        automap(self.struct, instance, keep, drop)

    def __getattr__(self, name):
        if name in self.struct:
            return self.struct[name]
        return super().__getattr__(name)


