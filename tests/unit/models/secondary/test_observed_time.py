from pytest import raises as assert_raises

from bundlebuilder.exceptions import ValidationError
from bundlebuilder.models import ObservedTime
from tests.unit.utils import utc_now_iso


def test_observed_time_validation_fails():
    observed_date_data = {
        'middle_time': 'This value will be ignored anyway, right?',
    }

    with assert_raises(ValidationError) as exc_info:
        ObservedTime(**observed_date_data)

    error = exc_info.value

    assert error.args == ({
        'start_time': ['Missing data for required field.'],
        'middle_time': ['Unknown field.'],
    },)


def test_observed_time_validation_succeeds():
    observed_date_data = {
        'start_time': utc_now_iso(),
        'end_time': utc_now_iso(),
    }

    observed_date = ObservedTime(**observed_date_data)

    assert observed_date.json == observed_date_data
