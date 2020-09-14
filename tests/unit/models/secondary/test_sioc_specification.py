from pytest import raises as assert_raises

from bundlebuilder.exceptions import ValidationError
from bundlebuilder.models import SIOCSpecification


def test_sioc_specification_validation_fails():
    sioc_specification_data = {}

    with assert_raises(ValidationError) as exc_info:
        SIOCSpecification(**sioc_specification_data)

    error = exc_info.value

    assert error.args == ({
        'SIOC': ['Missing data for required field.'],
    },)


def test_sioc_specification_validation_succeeds():
    sioc_specification_data = {
        'SIOC': 'SIOC',
    }

    sioc_specification = SIOCSpecification(**sioc_specification_data)

    sioc_specification_data['type'] = 'SIOC'

    assert sioc_specification.json == sioc_specification_data
