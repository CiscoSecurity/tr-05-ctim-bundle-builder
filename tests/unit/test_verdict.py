from pytest import raises as assert_raises

from bundlebuilder.constants import (
    DISPOSITION_MAP,
    OBSERVABLE_TYPE_CHOICES,
)
from bundlebuilder.exceptions import ValidationError
from bundlebuilder.models import Verdict
from .utils import utc_now_iso


def test_verdict_validation_fails():
    verdict_data = {
        'greeting': '¡Hola!',
        'disposition': 0,
        'observable': {
            'dangerous': False,
            'type': 'dummy',
        },
        'valid_time': {
            'middle_time': 'This value will be ignored anyway, right?',
            'end_time': '1970-01-01T00:00:00Z',
        },
        'disposition_name': 'Pristine',
    }

    with assert_raises(ValidationError) as exc_info:
        Verdict(**verdict_data)

    error = exc_info.value

    assert error.args == ({
        'greeting': ['Unknown field.'],
        'disposition': [
            f'Must be one of: {", ".join(map(repr, DISPOSITION_MAP.keys()))}.'
        ],
        'observable': {
            'dangerous': ['Unknown field.'],
            'type': [
                'Must be one of: '
                f'{", ".join(map(repr, OBSERVABLE_TYPE_CHOICES))}.'
            ],
            'value': ['Missing data for required field.'],
        },
        'valid_time': {
            'middle_time': ['Unknown field.'],
        },
        'disposition_name': [
            'Must be one of: '
            f'{", ".join(map(repr, DISPOSITION_MAP.values()))}.'
        ],
    },)


def test_verdict_validation_succeeds():
    verdict_data = {
        'disposition': 1,
        'observable': {'type': 'domain', 'value': 'cisco.com'},
        'valid_time': {'start_time': utc_now_iso()},
        'disposition_name': 'Clean',
    }

    verdict = Verdict(**verdict_data)

    type_ = 'verdict'

    assert verdict.json == {
        'type': type_,
        **verdict_data
    }
