from functools import partial

from ..entity import (
    EntitySchema,
    SecondaryEntity,
)
from ..fields import StringField
from ..validators import validate_string
from ...constants import OBSERVABLE_TYPE_CHOICES


class ObservableSchema(EntitySchema):
    type = StringField(
        validate=partial(validate_string, choices=OBSERVABLE_TYPE_CHOICES),
        required=True,
    )
    value = StringField(
        validate=validate_string,
        required=True,
    )


class Observable(SecondaryEntity):
    schema = ObservableSchema
