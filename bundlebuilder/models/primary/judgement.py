from functools import partial
from typing import (
    Iterator,
    Tuple,
)

from marshmallow.decorators import validates_schema
from marshmallow.exceptions import ValidationError

from ..entity import (
    EntitySchema,
    PrimaryEntity,
)
from ..fields import (
    StringField,
    IntegerField,
    EntityField,
    ListField,
    DateTimeField,
)
from ..secondary.external_reference import ExternalReference
from ..secondary.observable import Observable
from ..secondary.valid_time import ValidTime
from ..validators import (
    validate_string,
    validate_integer,
)
from ...constants import (
    CONFIDENCE_CHOICES,
    DISPOSITION_MAP,
    PRIORITY_MIN_VALUE,
    PRIORITY_MAX_VALUE,
    SEVERITY_CHOICES,
    SOURCE_MAX_LENGTH,
    LANGUAGE_MAX_LENGTH,
    REASON_MAX_LENGTH,
    REVISION_MIN_VALUE,
    TLP_CHOICES,
)


class JudgementSchema(EntitySchema):
    """
    https://github.com/threatgrid/ctim/blob/master/doc/structures/judgement.md
    """

    confidence = StringField(
        validate=partial(validate_string, choices=CONFIDENCE_CHOICES),
        required=True,
    )
    disposition = IntegerField(
        validate=partial(validate_integer, choices=DISPOSITION_MAP.keys()),
        required=True,
    )
    disposition_name = StringField(
        validate=partial(validate_string, choices=DISPOSITION_MAP.values()),
        required=True,
    )
    observable = EntityField(
        type=Observable,
        required=True,
    )
    priority = IntegerField(
        validate=partial(
            validate_integer,
            min_value=PRIORITY_MIN_VALUE,
            max_value=PRIORITY_MAX_VALUE,
        ),
        required=True,
    )
    severity = StringField(
        validate=partial(validate_string, choices=SEVERITY_CHOICES),
        required=True,
    )
    valid_time = EntityField(
        type=ValidTime,
        required=True,
    )
    external_references = ListField(
        EntityField(type=ExternalReference)
    )
    language = StringField(
        validate=partial(validate_string, max_length=LANGUAGE_MAX_LENGTH),
    )
    reason = StringField(
        validate=partial(validate_string, max_length=REASON_MAX_LENGTH),
    )
    reason_uri = StringField(
        validate=validate_string,
    )
    revision = IntegerField(
        validate=partial(validate_integer, min_value=REVISION_MIN_VALUE),
    )
    timestamp = DateTimeField()
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

    @validates_schema
    def validate_disposition_consistency(self, data, **kwargs):
        if not ('disposition' in data and 'disposition_name' in data):
            return

        if DISPOSITION_MAP[data['disposition']] != data['disposition_name']:
            message = (
                'Not a consistent disposition name for the specified '
                'disposition number. Must be '
                f'{DISPOSITION_MAP[data["disposition"]]!r}.'
            )
            raise ValidationError(message)


class Judgement(PrimaryEntity):
    schema = JudgementSchema

    def _generate_external_id_seed_values(self) -> Iterator[Tuple[str]]:
        yield (
            self.type,
            self.source,
            self.observable['value'],
            str(self.disposition),
            (self.timestamp or '').split('T', 1)[0],
        )
