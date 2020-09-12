from ..entity import (
    EntitySchema,
    SecondaryEntity,
)
from ..fields import (
    StringField,
    EntityField,
    MappingField,
    RawField,
)
from ..secondary.observable import Observable
from ..validators import validate_string


class ObservedRelationSchema(EntitySchema):
    """
    https://github.com/threatgrid/ctim/blob/master/doc/structures/sighting.md#observedrelation-object
    """

    origin = StringField(
        validate=validate_string,
        required=True,
    )
    related = EntityField(
        type=Observable,
        required=True,
    )
    relation = StringField(
        validate=validate_string,
        required=True,
    )
    source = EntityField(
        type=Observable,
        required=True,
    )
    origin_uri = StringField(
        validate=validate_string,
    )
    relation_info = MappingField(
        keys=StringField,
        values=RawField,
    )


class ObservedRelation(SecondaryEntity):
    schema = ObservedRelationSchema
