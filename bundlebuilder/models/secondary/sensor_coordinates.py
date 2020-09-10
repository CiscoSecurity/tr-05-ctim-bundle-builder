from marshmallow import fields

from ..entity import (
    EntitySchema,
    SecondaryEntity,
)
from ..fields import EntityField
from ..secondary.observable import Observable
from ..validators import validate_string


class SensorCoordinatesSchema(EntitySchema):
    observables = fields.List(
        EntityField(type=Observable),
        required=True,
    )
    type = fields.String(
        validate=validate_string,
        required=True,
    )
    os = fields.String(
        validate=validate_string,
    )


class SensorCoordinates(SecondaryEntity):
    schema = SensorCoordinatesSchema
