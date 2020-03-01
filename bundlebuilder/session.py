from collections import namedtuple
from contextlib import contextmanager
from functools import partial

from marshmallow import fields
from marshmallow.exceptions import (
    ValidationError as MarshmallowValidationError
)
from marshmallow.schema import Schema

from .constants import (
    SOURCE_MAX_LENGTH,
    DEFAULT_SESSION_EXTERNAL_ID_PREFIX,
    DEFAULT_SESSION_SOURCE,
    DEFAULT_SESSION_SOURCE_URI,
)
from .exceptions import (
    ValidationError as BundleBuilderValidationError
)
from .models.utils.validators import validate_string


class SessionSchema(Schema):
    external_id_prefix = fields.String(
        validate=validate_string,
        required=True,
    )
    source = fields.String(
        validate=partial(validate_string, max_length=SOURCE_MAX_LENGTH),
        required=True,
    )
    source_uri = fields.String(
        validate=validate_string,
        required=True,
    )


Session = namedtuple('Session', ('external_id_prefix', 'source', 'source_uri'))


def get_session() -> Session:
    return _SESSION


def get_default_session() -> Session:
    return _DEFAULT_SESSION


def set_session(external_id_prefix: str, source: str, source_uri: str) -> None:
    data = {
        'external_id_prefix': external_id_prefix,
        'source': source,
        'source_uri': source_uri,
    }

    try:
        data = SessionSchema().load(data)
    except MarshmallowValidationError as error:
        raise BundleBuilderValidationError(*error.args) from error

    global _SESSION
    _SESSION = Session(**data)


def set_default_session() -> None:
    global _SESSION
    _SESSION = _DEFAULT_SESSION


# Make each session a context manager being able to validate itself and set
# globally on `__enter__` + automatically switch back to the previous session
# on `__exit__` when used in `with` statements.


@contextmanager
def _set(session: Session):
    previous_session = get_session()
    try:
        # Validate the session before trying to set it globally.
        set_session(*session)
        yield
    finally:
        # The previous session is guaranteed to be valid anyway.
        global _SESSION
        _SESSION = previous_session


Session.set = lambda self: _set(self)


_DEFAULT_SESSION = Session(
    external_id_prefix=DEFAULT_SESSION_EXTERNAL_ID_PREFIX,
    source=DEFAULT_SESSION_SOURCE,
    source_uri=DEFAULT_SESSION_SOURCE_URI,
)
_SESSION = _DEFAULT_SESSION
