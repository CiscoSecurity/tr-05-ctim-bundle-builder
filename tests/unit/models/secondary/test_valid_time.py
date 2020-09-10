from pytest import raises as assert_raises

from bundlebuilder.exceptions import ValidationError
from bundlebuilder.models import ValidTime
from tests.unit.utils import utc_now_iso


def test_valid_time_validation_fails():
    valid_date_data = {
        'middle_time': 'This value will be ignored anyway, right?',
        'end_time': '1970-01-01T00:00:00Z',
    }

    with assert_raises(ValidationError) as exc_info:
        ValidTime(**valid_date_data)

    error = exc_info.value

    assert error.args == ({
        'middle_time': ['Unknown field.'],
    },)


def test_valid_time_validation_succeeds():
    valid_date_data = {
        'start_time': utc_now_iso(),
        'end_time': utc_now_iso(),
    }

    valid_date = ValidTime(**valid_date_data)

    assert valid_date.json == valid_date_data
