from functools import partial

from marshmallow import Schema, fields

from .entity import Entity
from .utils.fields import (
    EntityRefField,
)
from .utils.schemas import (
    ExternalReferenceSchema,
)
from .utils.validators import (
    validate_string,
    validate_integer,
    validate_datetime,
)
from ..constants import (
    RELATIONSHIP_TYPE_CHOICES,
    SCHEMA_VERSION,
    DESCRIPTION_MAX_LENGTH,
    LANGUAGE_MAX_LENGTH,
    REVISION_MIN_VALUE,
    SHORT_DESCRIPTION_LENGTH,
    SOURCE_MAX_LENGTH,
    TITLE_MAX_LENGTH,
    TLP_CHOICES,
)


class RelationshipSchema(Schema):
    id = fields.String(
        validate=validate_string,
    )
    relationship_type = fields.String(
        required=True,
        validate=partial(validate_string, choices=RELATIONSHIP_TYPE_CHOICES),
    )
    schema_version = fields.String(
        missing=SCHEMA_VERSION,
        validate=validate_string,
    )
    source_ref = EntityRefField(
        required=True,
        validate=validate_string,
    )
    target_ref = EntityRefField(
        required=True,
        validate=validate_string,
    )

    description = fields.String(
        validate=partial(validate_string, max_length=DESCRIPTION_MAX_LENGTH),
    )
    external_ids = fields.List(
        fields.String(
            validate=validate_string,
        )
    )
    external_references = fields.List(
        fields.Nested(ExternalReferenceSchema)
    )
    language = fields.String(
        validate=partial(validate_string, max_length=LANGUAGE_MAX_LENGTH),
    )
    revision = fields.Integer(
        validate=partial(validate_integer, min_value=REVISION_MIN_VALUE),
    )
    short_description = fields.String(
        validate=partial(validate_string, max_length=SHORT_DESCRIPTION_LENGTH),
    )
    source = fields.String(
        validate=partial(validate_string, max_length=SOURCE_MAX_LENGTH),
    )
    source_uri = fields.String(
        validate=validate_string,
    )
    timestamp = fields.String(
        validate=validate_datetime,
    )
    title = fields.String(
        validate=partial(validate_string, max_length=TITLE_MAX_LENGTH),
    )
    tlp = fields.String(
        validate=partial(validate_string, choices=TLP_CHOICES),
    )


class Relationship(Entity):
    schema = RelationshipSchema

    def generate_external_id_seed(self):
        # TODO: replace with real implementation
        return ''
