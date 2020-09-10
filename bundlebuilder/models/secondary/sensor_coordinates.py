from ..entity import (
    EntitySchema,
    SecondaryEntity,
)
from ..fields import (
    ListField,
    EntityField,
    StringField,
)
from ..secondary.observable import Observable
from ..validators import validate_string


class SensorCoordinatesSchema(EntitySchema):
    observables = ListField(
        EntityField(type=Observable),
        required=True,
    )
    type = StringField(
        validate=validate_string,
        required=True,
    )
    os = StringField(
        validate=validate_string,
    )


class SensorCoordinates(SecondaryEntity):
    schema = SensorCoordinatesSchema
