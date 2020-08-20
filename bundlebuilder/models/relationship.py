from functools import partial
from typing import (
    Iterator,
    Tuple,
)

from marshmallow import fields
from marshmallow.schema import Schema

from .entity import Entity
from .utils.fields import (
    EntityField,
    DateTimeField,
)
from .utils.schemas import (
    ExternalReferenceSchema,
)
from .utils.validators import (
    validate_string,
    validate_integer,
)
from ..constants import (
    DESCRIPTION_MAX_LENGTH,
    LANGUAGE_MAX_LENGTH,
    REVISION_MIN_VALUE,
    SHORT_DESCRIPTION_LENGTH,
    SOURCE_MAX_LENGTH,
    TITLE_MAX_LENGTH,
    TLP_CHOICES,
)


class RelationshipSchema(Schema):
    """
    https://github.com/threatgrid/ctim/blob/master/doc/structures/relationship.md
    """

    relationship_type = fields.String(
        validate=validate_string,
        required=True,
    )
    source_ref = EntityField(
        ref=True,
        validate=validate_string,
        required=True,
    )
    target_ref = EntityField(
        ref=True,
        validate=validate_string,
        required=True,
    )
    description = fields.String(
        validate=partial(validate_string, max_length=DESCRIPTION_MAX_LENGTH),
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
    timestamp = DateTimeField()
    title = fields.String(
        validate=partial(validate_string, max_length=TITLE_MAX_LENGTH),
    )
    tlp = fields.String(
        validate=partial(validate_string, choices=TLP_CHOICES),
    )

    source = fields.String(
        validate=partial(validate_string, max_length=SOURCE_MAX_LENGTH),
    )
    source_uri = fields.String(
        validate=validate_string,
    )

    external_id_salt_values = fields.List(
        fields.String(
            validate=validate_string,
        )
    )


class Relationship(Entity):
    schema = RelationshipSchema

    def generate_external_id_seed_values(self) -> Iterator[Tuple[str]]:
        yield (
            self.external_id_prefix,
            self.type,
        )
