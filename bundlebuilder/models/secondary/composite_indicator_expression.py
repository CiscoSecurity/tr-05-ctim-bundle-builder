from functools import partial

from marshmallow import fields

from ..entity import (
    EntitySchema,
    SecondaryEntity,
)
from ..validators import validate_string
from ...constants import BOOLEAN_OPERATOR_CHOICES


class CompositeIndicatorExpressionSchema(EntitySchema):
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


class CompositeIndicatorExpression(SecondaryEntity):
    schema = CompositeIndicatorExpressionSchema
