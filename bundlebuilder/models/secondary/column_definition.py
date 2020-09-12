from functools import partial

from ..entity import (
    EntitySchema,
    SecondaryEntity,
)
from ..fields import (
    StringField,
    BooleanField,
)
from ..validators import validate_string
from ...constants import (
    COLUMN_TYPE_CHOICES,
    DESCRIPTION_MAX_LENGTH,
    SHORT_DESCRIPTION_LENGTH,
)


class ColumnDefinitionSchema(EntitySchema):
    """
    https://github.com/threatgrid/ctim/blob/master/doc/structures/sighting.md#columndefinition-object
    """

    name = StringField(
        validate=validate_string,
        required=True,
    )
    type = StringField(
        validate=partial(validate_string, choices=COLUMN_TYPE_CHOICES),
        required=True,
    )
    description = StringField(
        validate=partial(validate_string, max_length=DESCRIPTION_MAX_LENGTH),
    )
    required = BooleanField()
    short_description = StringField(
        validate=partial(validate_string, max_length=SHORT_DESCRIPTION_LENGTH),
    )


class ColumnDefinition(SecondaryEntity):
    schema = ColumnDefinitionSchema
