from ..entity import (
    EntitySchema,
    SecondaryEntity,
)
from ..fields import (
    ListField,
    StringField,
)
from ..validators import validate_string


class ThreatBrainSpecificationSchema(EntitySchema):
    """
    https://github.com/threatgrid/ctim/blob/master/doc/structures/indicator.md#threatbrainspecification-object
    """

    variables = ListField(
        StringField(validate=validate_string),
        required=True,
    )
    query = StringField(
        validate=validate_string,
    )


class ThreatBrainSpecification(SecondaryEntity):
    schema = ThreatBrainSpecificationSchema

    def _initialize_missing_fields(self) -> None:
        super()._initialize_missing_fields()

        self.json = {
            'type': 'ThreatBrain',
            **self.json
        }
