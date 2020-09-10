from pytest import raises as assert_raises

from bundlebuilder.constants import DISPOSITION_MAP
from bundlebuilder.exceptions import ValidationError
from bundlebuilder.models import (
    Verdict,
    Observable,
)
from tests.unit.utils import utc_now_iso


def test_verdict_validation_fails():
    verdict_data = {
        'greeting': '¡Hola!',
        'disposition': 0,
        'observable': object(),
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
        'observable': ['Not a valid CTIM Observable.'],
        'valid_time': {
            'middle_time': ['Unknown field.'],
        },
        'disposition_name': [
            'Must be one of: '
            f'{", ".join(map(repr, DISPOSITION_MAP.values()))}.'
        ],
    },)


def test_verdict_validation_succeeds():
    observable = Observable(
        type='domain',
        value='cisco.com',
    )

    verdict_data = {
        'disposition': 1,
        'observable': observable,
        'valid_time': {'start_time': utc_now_iso()},
        'disposition_name': 'Clean',
    }

    verdict = Verdict(**verdict_data)

    verdict_data['observable'] = observable.json

    type_ = 'verdict'

    assert verdict.json == {
        'type': type_,
        **verdict_data
    }
