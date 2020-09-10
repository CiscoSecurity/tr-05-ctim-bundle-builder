from functools import partial

from marshmallow import fields

from ..entity import (
    EntitySchema,
    SecondaryEntity,
)
from ..validators import validate_string
from ...constants import (
    SOURCE_NAME_MAX_LENGTH,
    DESCRIPTION_MAX_LENGTH,
)


class ExternalReferenceSchema(EntitySchema):
    source_name = fields.String(
        validate=partial(validate_string, max_length=SOURCE_NAME_MAX_LENGTH),
        required=True,
    )
    description = fields.String(
        validate=partial(validate_string, max_length=DESCRIPTION_MAX_LENGTH),
    )
    external_id = fields.String(
        validate=validate_string,
    )
    hashes = fields.List(
        fields.String(
            validate=validate_string,
        )
    )
    url = fields.String(
        validate=validate_string,
    )


class ExternalReference(SecondaryEntity):
    schema = ExternalReferenceSchema
