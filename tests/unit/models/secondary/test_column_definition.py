from pytest import raises as assert_raises

from bundlebuilder.constants import (
    DESCRIPTION_MAX_LENGTH,
    COLUMN_TYPE_CHOICES,
    SHORT_DESCRIPTION_LENGTH,
)
from bundlebuilder.exceptions import ValidationError
from bundlebuilder.models import ColumnDefinition


def test_column_definition_validation_fails():
    column_definition_data = {
        'type': 'anything',
        'description': '\U0001f4a9' * DESCRIPTION_MAX_LENGTH,
        'required': 69,
        'short_description': '\U0001f4a9' * DESCRIPTION_MAX_LENGTH,
    }

    with assert_raises(ValidationError) as exc_info:
        ColumnDefinition(**column_definition_data)

    error = exc_info.value

    assert error.args == ({
        'name': ['Missing data for required field.'],
        'type': [
            'Must be one of: '
            f'{", ".join(map(repr, COLUMN_TYPE_CHOICES))}.'
        ],
        'required': ['Not a valid boolean.'],
        'short_description': [
            f'Must be at most {SHORT_DESCRIPTION_LENGTH} characters long.'
        ],
    },)


def test_column_definition_validation_succeeds():
    column_definition_data = {
        'name': 'id',
        'type': 'integer',
    }

    column_definition = ColumnDefinition(**column_definition_data)

    assert column_definition.json == column_definition_data
