from functools import partial

from marshmallow import fields

from ..entity import (
    EntitySchema,
    SecondaryEntity,
)
from ..fields import EntityField
from ..secondary.column_definition import ColumnDefinition
from ..validators import validate_integer
from ...constants import COUNT_MIN_VALUE


class SightingDataTableSchema(EntitySchema):
    columns = fields.List(
        EntityField(type=ColumnDefinition),
        required=True,
    )
    rows = fields.List(
        fields.List(fields.Raw),
        required=True,
    )
    row_count = fields.Integer(
        validate=partial(validate_integer, min_value=COUNT_MIN_VALUE),
    )


class SightingDataTable(SecondaryEntity):
    schema = SightingDataTableSchema
