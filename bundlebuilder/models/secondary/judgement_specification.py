from ..entity import (
    EntitySchema,
    SecondaryEntity,
)
from ..fields import (
    ListField,
    StringField,
    EntityField,
)
from ..secondary.related_judgement import RelatedJudgement
from ..validators import validate_string


class JudgementSpecificationSchema(EntitySchema):
    judgements = ListField(
        StringField(validate=validate_string),
        required=True,
    )
    required_judgements = ListField(
        EntityField(type=RelatedJudgement),
        required=True,
    )


class JudgementSpecification(SecondaryEntity):
    schema = JudgementSpecificationSchema

    def _initialize_missing_fields(self) -> None:
        super()._initialize_missing_fields()

        self.json = {
            'type': 'Judgement',
            **self.json
        }
