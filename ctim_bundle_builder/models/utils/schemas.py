from functools import partial

from marshmallow import Schema, fields

from .validators import validate_string
from ...constants import (
    SOURCE_NAME_MAX_LENGTH,
    DESCRIPTION_MAX_LENGTH,
)


class ExternalReferenceSchema(Schema):
    source_name = fields.String(
        required=True,
        validate=partial(validate_string, max_length=SOURCE_NAME_MAX_LENGTH),
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
