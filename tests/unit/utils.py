import re

from mock import MagicMock

from bundlebuilder.constants import EXTERNAL_ID_PREFIX


def mock_id(type):
    id_mock = MagicMock()

    id_re = re.compile(
        '^transient:{}-{}-[0-9a-z]{{64}}$'.format(
            EXTERNAL_ID_PREFIX, type
        )
    )
    id_mock.__eq__ = lambda self, other: (
        bool(id_re.match(other))
    )

    return id_mock


def mock_external_id(type):
    external_id_mock = MagicMock()

    external_id_re = re.compile(
        '^{}-{}-[0-9a-z]{{64}}$'.format(
            EXTERNAL_ID_PREFIX, type
        )
    )
    external_id_mock.__eq__ = lambda self, other: (
        bool(external_id_re.match(other))
    )

    return external_id_mock
