from functools import partial

from marshmallow import Schema, fields, validates_schema, ValidationError

from .entity import Entity
from .utils.schemas import (
    ObservableSchema,
    ValidTimeSchema,
    ExternalReferenceSchema,
)
from .utils.validators import (
    validate_string,
    validate_integer,
    validate_datetime,
)
from ..constants import (
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


class JudgementSchema(Schema):
    """
    https://github.com/threatgrid/ctim/blob/master/doc/structures/judgement.md
    """
    confidence = fields.String(
        validate=partial(validate_string, choices=CONFIDENCE_CHOICES),
        required=True,
    )
    disposition = fields.Integer(
        validate=partial(validate_integer, choices=DISPOSITION_MAP.keys()),
        required=True,
    )
    disposition_name = fields.String(
        validate=partial(validate_string, choices=DISPOSITION_MAP.values()),
        required=True,
    )
    id = fields.String(
        validate=validate_string,
    )
    observable = fields.Nested(
        ObservableSchema,
        required=True,
    )
    priority = fields.Integer(
        validate=partial(
            validate_integer,
            min_value=PRIORITY_MIN_VALUE,
            max_value=PRIORITY_MAX_VALUE,
        ),
        required=True,
    )
    severity = fields.String(
        validate=partial(validate_string, choices=SEVERITY_CHOICES),
        required=True,
    )
    source = fields.String(
        validate=partial(validate_string, max_length=SOURCE_MAX_LENGTH),
        required=True,
    )
    valid_time = fields.Nested(
        ValidTimeSchema,
        required=True,
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
    reason = fields.String(
        validate=partial(validate_string, max_length=REASON_MAX_LENGTH),
    )
    reason_uri = fields.String(
        validate=validate_string,
    )
    revision = fields.Integer(
        validate=partial(validate_integer, min_value=REVISION_MIN_VALUE),
    )
    source_uri = fields.String(
        validate=validate_string,
    )
    timestamp = fields.String(
        validate=validate_datetime,
    )
    tlp = fields.String(
        validate=partial(validate_string, choices=TLP_CHOICES),
    )

    @validates_schema
    def validate_disposition_consistency(self, data, **kwargs):
        if DISPOSITION_MAP[data['disposition']] != data['disposition_name']:
            message = (
                'Not a consistent disposition name for the specified '
                'disposition number. Must be {!r}.'.format(
                    DISPOSITION_MAP[data['disposition']]
                )
            )
            raise ValidationError(message)


class Judgement(Entity):
    schema = JudgementSchema

    def generate_external_id_seed(self):
        # TODO: replace with real implementation
        return ''
