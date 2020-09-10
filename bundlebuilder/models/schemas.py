from functools import partial

from marshmallow import fields
from marshmallow.decorators import post_load
from marshmallow.exceptions import ValidationError
from marshmallow.schema import Schema
from marshmallow.utils import (
    INCLUDE,
    RAISE,
)

from .validators import validate_string
from ..constants import (
    BOOLEAN_OPERATOR_CHOICES,
    CONFIDENCE_CHOICES,
    SPECIFICATION_TYPE_CHOICES,
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
