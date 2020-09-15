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
from ..secondary.observed_time import ObservedTime
from ..validators import validate_string


class IdentitySpecificationSchema(EntitySchema):
    """
    https://github.com/threatgrid/ctim/blob/master/doc/structures/sighting.md#identityspecification-object
    """

    observables = ListField(
        EntityField(type=Observable),
        required=True,
    )
    observed_time = EntityField(
        type=ObservedTime,
        required=True,
    )
    type = StringField(
        validate=validate_string,
        required=True,
    )
    os = StringField(
        validate=validate_string,
    )


class IdentitySpecification(SecondaryEntity):
    schema = IdentitySpecificationSchema
