from marshmallow import fields

from ..entity import (
    EntitySchema,
    SecondaryEntity,
)
from ..fields import EntityField
from ..secondary.observable import Observable
from ..secondary.observed_time import ObservedTime
from ..validators import validate_string


class IdentitySpecificationSchema(EntitySchema):
    observables = fields.List(
        EntityField(type=Observable),
        required=True,
    )
    observed_time = EntityField(
        type=ObservedTime,
        required=True,
    )
    type = fields.String(
        validate=validate_string,
        required=True,
    )
    os = fields.String(
        validate=validate_string,
    )


class IdentitySpecification(SecondaryEntity):
    schema = IdentitySpecificationSchema
