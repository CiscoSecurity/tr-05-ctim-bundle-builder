from functools import partial

from marshmallow import fields
from marshmallow.decorators import post_load
from marshmallow.exceptions import ValidationError
from marshmallow.schema import Schema
from marshmallow.utils import (
    INCLUDE,
    RAISE,
)

from .validators import (
    validate_string,
    validate_integer,
)
from ..constants import (
    DESCRIPTION_MAX_LENGTH,
    COLUMN_TYPE_CHOICES,
    SHORT_DESCRIPTION_LENGTH,
    COUNT_MIN_VALUE,
    OBSERVABLE_TYPE_CHOICES,
    BOOLEAN_OPERATOR_CHOICES,
    CONFIDENCE_CHOICES,
    SPECIFICATION_TYPE_CHOICES,
)


class ColumnDefinitionSchema(Schema):
    name = fields.String(
        validate=validate_string,
        required=True,
    )
    type = fields.String(
        validate=partial(validate_string, choices=COLUMN_TYPE_CHOICES),
        required=True,
    )
    description = fields.String(
        validate=partial(validate_string, max_length=DESCRIPTION_MAX_LENGTH)
    )
    required = fields.Boolean()
    short_description = fields.String(
        validate=partial(validate_string, max_length=SHORT_DESCRIPTION_LENGTH),
    )


class SightingDataTableSchema(Schema):
    columns = fields.List(
        fields.Nested(ColumnDefinitionSchema),
        required=True,
    )
    rows = fields.List(
        fields.List(fields.Raw),
        required=True,
    )
    row_count = fields.Integer(
        validate=partial(validate_integer, min_value=COUNT_MIN_VALUE)
    )


class ObservableSchema(Schema):
    type = fields.String(
        validate=partial(validate_string, choices=OBSERVABLE_TYPE_CHOICES),
        required=True,
    )
    value = fields.String(
        validate=validate_string,
        required=True,
    )


class SensorCoordinatesSchema(Schema):
    observables = fields.List(
        fields.Nested(ObservableSchema),
        required=True,
    )
    type = fields.String(
        validate=validate_string,
        required=True,
    )
    os = fields.String(
        validate=validate_string,
    )


class IdentitySpecificationSchema(Schema):
    observables = fields.List(
        fields.Nested(ObservableSchema),
        required=True,
    )
    # observed_time = fields.Nested(
    #     ObservedTimeSchema,
    #     required=True,
    # )
    type = fields.String(
        validate=validate_string,
        required=True,
    )
    os = fields.String(
        validate=validate_string,
    )


class CompositeIndicatorExpressionSchema(Schema):
    indicator_ids = fields.List(
        fields.String(
            validate=validate_string,
        ),
        required=True,
    )
    operator = fields.String(
        validate=partial(validate_string, choices=BOOLEAN_OPERATOR_CHOICES),
        required=True,
    )


class KillChainPhaseSchema(Schema):
    kill_chain_name = fields.String(
        validate=validate_string,
        required=True,
    )
    phase_name = fields.String(
        validate=validate_string,
        required=True,
    )

    @post_load
    def normalize_names(self, data, **kwargs):
        for field in ('kill_chain_name', 'phase_name'):
            if field in data:
                value = data[field]
                value = value.lower().strip().split()
                value = ' '.join(value)
                value = value.replace(' ', '_').replace('_', '-')
                data[field] = value
        return data


class BaseSpecificationSchema(Schema):
    pass


class RelatedJudgementSchema(Schema):
    judgement_id = fields.String(
        validate=validate_string,
        required=True,
    )
    confidence = fields.String(
        validate=partial(validate_string, choices=CONFIDENCE_CHOICES),
    )
    relationship = fields.String(
        validate=validate_string,
    )
    source = fields.String(
        validate=validate_string,
    )


class JudgementSpecificationSchema(BaseSpecificationSchema):
    judgements = fields.List(
        fields.String(
            validate=validate_string,
        ),
        required=True,
    )
    required_judgements = fields.List(
        fields.Nested(RelatedJudgementSchema),
        required=True,
    )


class ThreatBrainSpecificationSchema(BaseSpecificationSchema):
    variables = fields.List(
        fields.String(
            validate=validate_string,
        ),
        required=True,
    )
    query = fields.String(
        validate=validate_string,
    )


class SnortSpecificationSchema(BaseSpecificationSchema):
    snort_sig = fields.String(
        validate=validate_string,
        required=True,
    )


class SIOCSpecificationSchema(BaseSpecificationSchema):
    SIOC = fields.String(
        validate=validate_string,
        required=True,
    )


class OpenIOCSpecificationSchema(BaseSpecificationSchema):
    open_IOC = fields.String(
        validate=validate_string,
        required=True,
    )


SPECIFICATION_SCHEMA_MAP = dict(
    zip(SPECIFICATION_TYPE_CHOICES, BaseSpecificationSchema.__subclasses__())
)


class SpecificationSchema(Schema):
    type = fields.String(
        validate=partial(validate_string, choices=SPECIFICATION_TYPE_CHOICES),
        required=True,
    )

    def load(self, data, **kwargs):
        kwargs['partial'] = False
        kwargs['unknown'] = INCLUDE

        data = super().load(data, **kwargs)

        singleton = False

        if not isinstance(data, list):
            singleton = True
            data = [data]

        message = {}

        kwargs['many'] = False
        kwargs['unknown'] = RAISE

        for index, _ in enumerate(data):
            schema = SPECIFICATION_SCHEMA_MAP[data[index]['type']]

            try:
                data[index] = {
                    'type': data[index].pop('type'),
                    **schema().load(data[index], **kwargs)
                }
            except ValidationError as error:
                message[index] = error.messages

        if message:
            raise ValidationError(message[0] if singleton else message)

        return data[0] if singleton else data
