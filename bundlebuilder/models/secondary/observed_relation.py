from marshmallow import fields

from ..fields import EntityField
from ..entity import (
    EntitySchema,
    SecondaryEntity,
)
from ..secondary.observable import Observable
from ..validators import validate_string


class ObservedRelationSchema(EntitySchema):
    origin = fields.String(
        validate=validate_string,
        required=True,
    )
    related = EntityField(
        type=Observable,
        required=True,
    )
    relation = fields.String(
        validate=validate_string,
        required=True,
    )
    source = EntityField(
        type=Observable,
        required=True,
    )
    origin_uri = fields.String(
        validate=validate_string,
    )
    relation_info = fields.Mapping(
        keys=fields.String,
        values=fields.Raw,
    )


class ObservedRelation(SecondaryEntity):
    schema = ObservedRelationSchema
