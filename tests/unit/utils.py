import datetime as dt
import re
from unittest.mock import MagicMock


def mock_transient_id(external_id_prefix, type):
    id_mock = MagicMock()

    id_re = re.compile(
        f'^transient:{external_id_prefix}-{type}-[0-9a-z]{{32}}$'
    )
    id_mock.__eq__ = lambda self, other: (
        bool(id_re.match(other))
    )

    return id_mock


def mock_external_id(external_id_prefix, type):
    external_id_mock = MagicMock()

    external_id_re = re.compile(
        f'^{external_id_prefix}-{type}-[0-9a-z]{{64}}$'
    )
    external_id_mock.__eq__ = lambda self, other: (
        bool(external_id_re.match(other))
    )

    return external_id_mock


def utc_now_iso():
    # Python datetime objects don't have time zone info by default,
    # and without it, Python actually violates the ISO 8601 specification.
    return dt.datetime.utcnow().isoformat(timespec='milliseconds') + 'Z'
