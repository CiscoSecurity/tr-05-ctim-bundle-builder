from pytest import raises as assert_raises

from bundlebuilder.exceptions import ValidationError
from bundlebuilder.models import SnortSpecification


def test_snort_specification_validation_fails():
    snort_specification_data = {}

    with assert_raises(ValidationError) as exc_info:
        SnortSpecification(**snort_specification_data)

    error = exc_info.value

    assert error.args == ({
        'snort_sig': ['Missing data for required field.'],
    },)


def test_snort_specification_validation_succeeds():
    snort_specification_data = {
        'snort_sig': 'abracadabra',
    }

    snort_specification = SnortSpecification(**snort_specification_data)

    snort_specification_data['type'] = 'Snort'

    assert snort_specification.json == snort_specification_data
