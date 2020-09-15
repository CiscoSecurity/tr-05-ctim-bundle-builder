from functools import partial

from ..entity import (
    EntitySchema,
    SecondaryEntity,
)
from ..fields import StringField
from ..validators import validate_string
from ...constants import CONFIDENCE_CHOICES


class RelatedJudgementSchema(EntitySchema):
    """
    https://github.com/threatgrid/ctim/blob/master/doc/structures/indicator.md#relatedjudgement-object
    """

    judgement_id = StringField(
        validate=validate_string,
        required=True,
    )
    confidence = StringField(
        validate=partial(validate_string, choices=CONFIDENCE_CHOICES),
    )
    relationship = StringField(
        validate=validate_string,
    )
    source = StringField(
        validate=validate_string,
    )


class RelatedJudgement(SecondaryEntity):
    schema = RelatedJudgementSchema
