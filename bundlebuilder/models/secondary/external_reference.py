from functools import partial

from ..entity import (
    EntitySchema,
    SecondaryEntity,
)
from ..fields import (
    StringField,
    ListField,
)
from ..validators import validate_string
from ...constants import (
    SOURCE_NAME_MAX_LENGTH,
    DESCRIPTION_MAX_LENGTH,
)


class ExternalReferenceSchema(EntitySchema):
    """
    https://github.com/threatgrid/ctim/blob/master/doc/structures/bundle.md#externalreference-object
    https://github.com/threatgrid/ctim/blob/master/doc/structures/indicator.md#externalreference-object
    https://github.com/threatgrid/ctim/blob/master/doc/structures/judgement.md#externalreference-object
    https://github.com/threatgrid/ctim/blob/master/doc/structures/relationship.md#externalreference-object
    https://github.com/threatgrid/ctim/blob/master/doc/structures/sighting.md#externalreference-object
    https://github.com/threatgrid/ctim/blob/master/doc/structures/verdict.md#externalreference-object
    """

    source_name = StringField(
        validate=partial(validate_string, max_length=SOURCE_NAME_MAX_LENGTH),
        required=True,
    )
    description = StringField(
        validate=partial(validate_string, max_length=DESCRIPTION_MAX_LENGTH),
    )
    external_id = StringField(
        validate=validate_string,
    )
    hashes = ListField(
        StringField(validate=validate_string)
    )
    url = StringField(
        validate=validate_string,
    )


class ExternalReference(SecondaryEntity):
    schema = ExternalReferenceSchema
