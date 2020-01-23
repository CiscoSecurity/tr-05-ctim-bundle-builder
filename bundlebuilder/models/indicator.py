from functools import partial
from typing import List

from marshmallow import fields
from marshmallow.schema import Schema

from .entity import Entity
from .utils.fields import DateTimeField
from .utils.schemas import (
    ValidTimeSchema,
    CompositeIndicatorExpressionSchema,
    ExternalReferenceSchema,
    KillChainPhaseSchema,
    SpecificationSchema,
)
from .utils.validators import (
    validate_string,
    validate_integer,
)
from ..constants import (
    PRODUCER_MAX_LENGTH,
    CONFIDENCE_CHOICES,
    DESCRIPTION_MAX_LENGTH,
    INDICATOR_TYPE_CHOICES,
    LANGUAGE_MAX_LENGTH,
    LIKELY_IMPACT_MAX_LENGTH,
    REVISION_MIN_VALUE,
    SEVERITY_CHOICES,
    SHORT_DESCRIPTION_LENGTH,
    TAG_MAX_LENGTH,
    TEST_MECHANISM_MAX_LENGTH,
    TITLE_MAX_LENGTH,
    TLP_CHOICES,
)


class IndicatorSchema(Schema):
    """
    https://github.com/threatgrid/ctim/blob/master/doc/structures/indicator.md
    """
    producer = fields.String(
        validate=partial(validate_string, max_length=PRODUCER_MAX_LENGTH),
        required=True,
    )
    valid_time = fields.Nested(
        ValidTimeSchema,
        required=True,
    )
    composite_indicator_expression = fields.Nested(
        CompositeIndicatorExpressionSchema
    )
    confidence = fields.String(
        validate=partial(validate_string, choices=CONFIDENCE_CHOICES),
    )
    description = fields.String(
        validate=partial(validate_string, max_length=DESCRIPTION_MAX_LENGTH),
    )
    external_references = fields.List(
        fields.Nested(ExternalReferenceSchema)
    )
    indicator_type = fields.List(
        fields.String(
            validate=partial(validate_string, choices=INDICATOR_TYPE_CHOICES),
        )
    )
    kill_chain_phases = fields.List(
        fields.Nested(KillChainPhaseSchema)
    )
    language = fields.String(
        validate=partial(validate_string, max_length=LANGUAGE_MAX_LENGTH),
    )
    likely_impact = fields.String(
        validate=partial(validate_string, max_length=LIKELY_IMPACT_MAX_LENGTH),
    )
    negate = fields.Boolean()
    revision = fields.Integer(
        validate=partial(validate_integer, min_value=REVISION_MIN_VALUE),
    )
    severity = fields.String(
        validate=partial(validate_string, choices=SEVERITY_CHOICES),
    )
    short_description = fields.String(
        validate=partial(validate_string, max_length=SHORT_DESCRIPTION_LENGTH),
    )
    specification = fields.Nested(SpecificationSchema)
    tags = fields.List(
        fields.String(
            validate=partial(validate_string, max_length=TAG_MAX_LENGTH),
        )
    )
    test_mechanisms = fields.List(
        fields.String(
            validate=partial(
                validate_string,
                max_length=TEST_MECHANISM_MAX_LENGTH,
            ),
        )
    )
    timestamp = DateTimeField()
    title = fields.String(
        validate=partial(validate_string, max_length=TITLE_MAX_LENGTH),
    )
    tlp = fields.String(
        validate=partial(validate_string, choices=TLP_CHOICES),
    )

    external_id_extra_values = fields.List(
        fields.String(
            validate=validate_string,
        )
    )


class Indicator(Entity):
    schema = IndicatorSchema

    @property
    def external_id_seed_values(self) -> List[str]:
        return [
            self.external_id_prefix,
            self.type,
            self.title,
            self.producer,
        ]
