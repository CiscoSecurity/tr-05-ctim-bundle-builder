from functools import partial

from marshmallow import fields

from ..entity import (
    EntitySchema,
    SecondaryEntity,
)
from ..validators import validate_string
from ...constants import (
    COLUMN_TYPE_CHOICES,
    DESCRIPTION_MAX_LENGTH,
    SHORT_DESCRIPTION_LENGTH,
)


class ColumnDefinitionSchema(EntitySchema):
    name = fields.String(
        validate=validate_string,
        required=True,
    )
    type = fields.String(
        validate=partial(validate_string, choices=COLUMN_TYPE_CHOICES),
        required=True,
    )
    description = fields.String(
        validate=partial(validate_string, max_length=DESCRIPTION_MAX_LENGTH),
    )
    required = fields.Boolean()
    short_description = fields.String(
        validate=partial(validate_string, max_length=SHORT_DESCRIPTION_LENGTH),
    )


class ColumnDefinition(SecondaryEntity):
    schema = ColumnDefinitionSchema
