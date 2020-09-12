from pytest import raises as assert_raises

from bundlebuilder.exceptions import ValidationError
from bundlebuilder.models import OpenIOCSpecification


def test_open_ioc_specification_validation_fails():
    open_ioc_specification_data = {}

    with assert_raises(ValidationError) as exc_info:
        OpenIOCSpecification(**open_ioc_specification_data)

    error = exc_info.value

    assert error.args == ({
        'open_IOC': ['Missing data for required field.'],
    },)


def test_open_ioc_specification_validation_succeeds():
    open_ioc_specification_data = {
        'open_IOC': 'abracadabra',
    }

    open_ioc_specification = OpenIOCSpecification(
        **open_ioc_specification_data
    )

    open_ioc_specification_data['type'] = 'OpenIOC'

    assert open_ioc_specification.json == open_ioc_specification_data
