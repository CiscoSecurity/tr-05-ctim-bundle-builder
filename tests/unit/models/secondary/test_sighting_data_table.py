from pytest import raises as assert_raises

from bundlebuilder.constants import COUNT_MIN_VALUE
from bundlebuilder.exceptions import ValidationError
from bundlebuilder.models import (
    SightingDataTable,
    ColumnDefinition,
)


def test_sighting_data_table_validation_fails():
    sighting_data_table_data = {
        'column_count': +1,
        'columns': [object()],
        'rows': [object()],
        'row_count': -1,
    }

    with assert_raises(ValidationError) as exc_info:
        SightingDataTable(**sighting_data_table_data)

    error = exc_info.value

    assert error.args == ({
        'column_count': ['Unknown field.'],
        'columns': {
            0: ['Not a valid CTIM ColumnDefinition.'],
        },
        'rows': {
            0: ['Not a valid list.'],
        },
        'row_count': [
            f'Must be greater than or equal to {COUNT_MIN_VALUE}.'
        ],
    },)


def test_sighting_data_table_validation_succeeds():
    columns = [
        ColumnDefinition(
            name='full_name',
            type='string',
            required=True,
        ),
        ColumnDefinition(
            name='country',
            type='string',
            required=False,
        ),
        ColumnDefinition(
            name='year_of_birth',
            type='integer',
            required=False,
        ),
    ]

    rows = [
        ['Gevorg Davoian', 'Ukraine', 1993],
    ]

    sighting_data_table_data = {
        'columns': columns,
        'rows': rows,
    }

    sighting_data_table = SightingDataTable(**sighting_data_table_data)

    sighting_data_table_data['columns'] = [column.json for column in columns]

    assert sighting_data_table.json == sighting_data_table_data
