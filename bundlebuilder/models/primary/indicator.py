from functools import partial
from typing import (
    Iterator,
    Tuple,
)

from marshmallow import fields

from ..fields import (
    EntityField,
    DateTimeField,
)
from ..entity import (
    EntitySchema,
    PrimaryEntity,
)
from ..secondary.composite_indicator_expression import (
    CompositeIndicatorExpression
)
from ..secondary.external_reference import ExternalReference
from ..secondary.valid_time import ValidTime
from ..schemas import (
    KillChainPhaseSchema,
    SpecificationSchema,
)
from ..validators import (
    validate_string,
    validate_integer,
)
from ...constants import (
    PRODUCER_MAX_LENGTH,
    CONFIDENCE_CHOICES,
    DESCRIPTION_MAX_LENGTH,
    INDICATOR_TYPE_CHOICES,
    LANGUAGE_MAX_LENGTH,
    LIKELY_IMPACT_MAX_LENGTH,
    REVISION_MIN_VALUE,
    SEVERITY_CHOICES,
    SHORT_DESCRIPTION_LENGTH,
    SOURCE_MAX_LENGTH,
    TAG_MAX_LENGTH,
    TEST_MECHANISM_MAX_LENGTH,
    TITLE_MAX_LENGTH,
    TLP_CHOICES,
)


class IndicatorSchema(EntitySchema):
    """
    https://github.com/threatgrid/ctim/blob/master/doc/structures/indicator.md
    """

    producer = fields.String(
        validate=partial(validate_string, max_length=PRODUCER_MAX_LENGTH),
        required=True,
    )
    valid_time = EntityField(
        type=ValidTime,
        required=True,
    )
    composite_indicator_expression = EntityField(
        type=CompositeIndicatorExpression,
    )
    confidence = fields.String(
        validate=partial(validate_string, choices=CONFIDENCE_CHOICES),
    )
    description = fields.String(
        validate=partial(validate_string, max_length=DESCRIPTION_MAX_LENGTH),
    )
    external_references = fields.List(
        EntityField(type=ExternalReference)
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
    external_ids = fields.List(
        fields.String(
            validate=validate_string,
        )
    )


class Indicator(PrimaryEntity):
    schema = IndicatorSchema

    def _generate_external_id_seed_values(self) -> Iterator[Tuple[str]]:
        yield (
            self.type,
            self.title or '',
            self.producer,
        )
