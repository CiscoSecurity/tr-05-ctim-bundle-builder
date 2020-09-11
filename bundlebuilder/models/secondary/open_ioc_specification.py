from ..entity import (
    EntitySchema,
    SecondaryEntity,
)
from ..fields import StringField
from ..validators import validate_string


class OpenIOCSpecificationSchema(EntitySchema):
    """
    https://github.com/threatgrid/ctim/blob/master/doc/structures/indicator.md#openiocspecification-object
    """

    open_IOC = StringField(
        validate=validate_string,
        required=True,
    )


class OpenIOCSpecification(SecondaryEntity):
    schema = OpenIOCSpecificationSchema

    def _initialize_missing_fields(self) -> None:
        super()._initialize_missing_fields()

        self.json = {
            'type': 'OpenIOC',
            **self.json
        }
