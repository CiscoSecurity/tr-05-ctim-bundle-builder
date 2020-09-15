from pytest import raises as assert_raises

from bundlebuilder.constants import DISPOSITION_MAP
from bundlebuilder.exceptions import ValidationError
from bundlebuilder.models import (
    Verdict,
    Observable,
    ValidTime,
)
from tests.unit.utils import utc_now_iso


def test_verdict_validation_fails():
    verdict_data = {
        'greeting': '¡Hola!',
        'disposition': 0,
        'observable': object(),
        'valid_time': object(),
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
        'valid_time': ['Not a valid CTIM ValidTime.'],
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

    valid_time = ValidTime(
        start_time=utc_now_iso(),
        end_time=utc_now_iso(),
    )

    verdict_data = {
        'disposition': 1,
        'observable': observable,
        'valid_time': valid_time,
        'disposition_name': 'Clean',
    }

    verdict = Verdict(**verdict_data)

    verdict_data['observable'] = observable.json
    verdict_data['valid_time'] = valid_time.json

    type_ = 'verdict'

    assert verdict.json == {
        'type': type_,
        **verdict_data
    }
