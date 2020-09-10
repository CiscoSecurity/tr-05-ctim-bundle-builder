from pytest import raises as assert_raises

from bundlebuilder.exceptions import ValidationError
from bundlebuilder.models import ExternalReference


def test_external_reference_validation_fails():
    external_reference_data = {
        'description': '',
        'external_id': None,
        'hashes': ['alpha', 'beta', 'gamma'],
    }

    with assert_raises(ValidationError) as exc_info:
        ExternalReference(**external_reference_data)

    error = exc_info.value

    assert error.args == ({
        'description': ['Field may not be blank.'],
        'external_id': ['Field may not be null.'],
        'source_name': ['Missing data for required field.'],
    },)


def test_external_reference_validation_succeeds():
    external_reference_data = {
        'source_name': 'Hello, world!',
        'description': 'No comment...',
        'external_id': '123-456-789',
    }

    external_reference = ExternalReference(**external_reference_data)

    assert external_reference.json == external_reference_data
