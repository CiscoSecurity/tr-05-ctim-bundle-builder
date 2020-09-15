from ..entity import (
    EntitySchema,
    SecondaryEntity,
)
from ..fields import StringField
from ..validators import validate_string


class SnortSpecificationSchema(EntitySchema):
    """
    https://github.com/threatgrid/ctim/blob/master/doc/structures/indicator.md#snortspecification-object
    """

    snort_sig = StringField(
        validate=validate_string,
        required=True,
    )


class SnortSpecification(SecondaryEntity):
    schema = SnortSpecificationSchema

    def _initialize_missing_fields(self) -> None:
        super()._initialize_missing_fields()

        self.json = {
            'type': 'Snort',
            **self.json
        }
