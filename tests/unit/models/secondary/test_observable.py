from pytest import raises as assert_raises

from bundlebuilder.constants import OBSERVABLE_TYPE_CHOICES
from bundlebuilder.exceptions import ValidationError
from bundlebuilder.models import Observable


def test_observable_validation_fails():
    observable_data = {
        'dangerous': False,
        'type': 'dummy',
    }

    with assert_raises(ValidationError) as exc_info:
        Observable(**observable_data)

    error = exc_info.value

    assert error.args == ({
        'dangerous': ['Unknown field.'],
        'type': [
            'Must be one of: '
            f'{", ".join(map(repr, OBSERVABLE_TYPE_CHOICES))}.'
        ],
        'value': ['Missing data for required field.'],
    },)


def test_observable_validation_succeeds():
    observable_data = {
        'type': 'domain',
        'value': 'cisco.com',
    }

    observable = Observable(**observable_data)

    assert observable.json == observable_data
