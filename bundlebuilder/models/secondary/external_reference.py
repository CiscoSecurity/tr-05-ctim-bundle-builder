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
        StringField(
            validate=validate_string,
        )
    )
    url = StringField(
        validate=validate_string,
    )


class ExternalReference(SecondaryEntity):
    schema = ExternalReferenceSchema
