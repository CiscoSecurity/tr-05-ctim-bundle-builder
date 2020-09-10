from functools import partial

from marshmallow import fields

from ..entity import (
    EntitySchema,
    SecondaryEntity,
)
from ..validators import validate_string
from ...constants import OBSERVABLE_TYPE_CHOICES


class ObservableSchema(EntitySchema):
    type = fields.String(
        validate=partial(validate_string, choices=OBSERVABLE_TYPE_CHOICES),
        required=True,
    )
    value = fields.String(
        validate=validate_string,
        required=True,
    )


class Observable(SecondaryEntity):
    schema = ObservableSchema
