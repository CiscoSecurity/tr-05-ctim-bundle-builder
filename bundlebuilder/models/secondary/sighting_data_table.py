from functools import partial

from ..entity import (
    EntitySchema,
    SecondaryEntity,
)
from ..fields import (
    ListField,
    EntityField,
    RawField,
    IntegerField,
)
from ..secondary.column_definition import ColumnDefinition
from ..validators import validate_integer
from ...constants import COUNT_MIN_VALUE


class SightingDataTableSchema(EntitySchema):
    """
    https://github.com/threatgrid/ctim/blob/master/doc/structures/sighting.md#sightingdatatable-object
    """

    columns = ListField(
        EntityField(type=ColumnDefinition),
        required=True,
    )
    rows = ListField(
        ListField(RawField),
        required=True,
    )
    row_count = IntegerField(
        validate=partial(validate_integer, min_value=COUNT_MIN_VALUE),
    )


class SightingDataTable(SecondaryEntity):
    schema = SightingDataTableSchema
