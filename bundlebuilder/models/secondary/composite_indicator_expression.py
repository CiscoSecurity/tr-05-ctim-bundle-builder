from functools import partial

from ..entity import (
    EntitySchema,
    SecondaryEntity,
)
from ..fields import (
    ListField,
    StringField,
)
from ..validators import validate_string
from ...constants import BOOLEAN_OPERATOR_CHOICES


class CompositeIndicatorExpressionSchema(EntitySchema):
    indicator_ids = ListField(
        StringField(validate=validate_string),
        required=True,
    )
    operator = StringField(
        validate=partial(validate_string, choices=BOOLEAN_OPERATOR_CHOICES),
        required=True,
    )


class CompositeIndicatorExpression(SecondaryEntity):
    schema = CompositeIndicatorExpressionSchema
