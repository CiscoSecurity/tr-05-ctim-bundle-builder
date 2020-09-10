from functools import partial
from typing import (
    Iterator,
    Tuple,
)

from ..entity import (
    EntitySchema,
    PrimaryEntity,
)
from ..fields import (
    StringField,
    EntityField,
    ListField,
    IntegerField,
    DateTimeField,
)
from ..secondary.external_reference import ExternalReference
from ..validators import (
    validate_string,
    validate_integer,
)
from ...constants import (
    DESCRIPTION_MAX_LENGTH,
    LANGUAGE_MAX_LENGTH,
    REVISION_MIN_VALUE,
    SHORT_DESCRIPTION_LENGTH,
    SOURCE_MAX_LENGTH,
    TITLE_MAX_LENGTH,
    TLP_CHOICES,
)


class RelationshipSchema(EntitySchema):
    """
    https://github.com/threatgrid/ctim/blob/master/doc/structures/relationship.md
    """

    relationship_type = StringField(
        validate=validate_string,
        required=True,
    )
    source_ref = EntityField(
        type=PrimaryEntity,
        type_name='Entity',
        ref=True,
        validate=validate_string,
        required=True,
    )
    target_ref = EntityField(
        type=PrimaryEntity,
        type_name='Entity',
        ref=True,
        validate=validate_string,
        required=True,
    )
    description = StringField(
        validate=partial(validate_string, max_length=DESCRIPTION_MAX_LENGTH),
    )
    external_references = ListField(
        EntityField(type=ExternalReference)
    )
    language = StringField(
        validate=partial(validate_string, max_length=LANGUAGE_MAX_LENGTH),
    )
    revision = IntegerField(
        validate=partial(validate_integer, min_value=REVISION_MIN_VALUE),
    )
    short_description = StringField(
        validate=partial(validate_string, max_length=SHORT_DESCRIPTION_LENGTH),
    )
    timestamp = DateTimeField()
    title = StringField(
        validate=partial(validate_string, max_length=TITLE_MAX_LENGTH),
    )
    tlp = StringField(
        validate=partial(validate_string, choices=TLP_CHOICES),
    )

    source = StringField(
        validate=partial(validate_string, max_length=SOURCE_MAX_LENGTH),
    )
    source_uri = StringField(
        validate=validate_string,
    )

    external_id_salt_values = ListField(
        StringField(
            validate=validate_string,
        )
    )
    external_ids = ListField(
        StringField(
            validate=validate_string,
        )
    )


class Relationship(PrimaryEntity):
    schema = RelationshipSchema

    def _generate_external_id_seed_values(self) -> Iterator[Tuple[str]]:
        yield (
            self.type,
        )
