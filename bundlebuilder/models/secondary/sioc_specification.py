from ..entity import (
    EntitySchema,
    SecondaryEntity,
)
from ..fields import StringField
from ..validators import validate_string


class SIOCSpecificationSchema(EntitySchema):
    """
    https://github.com/threatgrid/ctim/blob/master/doc/structures/indicator.md#siocspecification-object
    """

    SIOC = StringField(
        validate=validate_string,
        required=True,
    )


class SIOCSpecification(SecondaryEntity):
    schema = SIOCSpecificationSchema

    def _initialize_missing_fields(self) -> None:
        super()._initialize_missing_fields()

        self.json = {
            'type': 'SIOC',
            **self.json
        }
