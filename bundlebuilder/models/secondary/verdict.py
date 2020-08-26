from functools import partial

from marshmallow import fields
from marshmallow.decorators import validates_schema
from marshmallow.exceptions import (
    ValidationError as MarshmallowValidationError
)

from ..fields import EntityField
from ..entity import (
    EntitySchema,
    SecondaryEntity,
)
from ..primary.judgement import Judgement
from ..schemas import (
    ObservableSchema,
    ValidTimeSchema,
)
from ..validators import (
    validate_integer,
    validate_string,
)
from ...constants import DISPOSITION_MAP
from ...exceptions import (
    ValidationError as BundleBuilderValidationError
)


class VerdictSchema(EntitySchema):
    """
    https://github.com/threatgrid/ctim/blob/master/doc/structures/verdict.md
    """

    disposition = fields.Integer(
        validate=partial(validate_integer, choices=DISPOSITION_MAP.keys()),
        required=True,
    )
    observable = fields.Nested(
        ObservableSchema,
        required=True,
    )
    valid_time = fields.Nested(
        ValidTimeSchema,
        required=True,
    )
    disposition_name = fields.String(
        validate=partial(validate_string, choices=DISPOSITION_MAP.values()),
    )

    @validates_schema
    def validate_disposition_consistency(self, data, **kwargs):
        if not ('disposition' in data and 'disposition_name' in data):
            return

        if DISPOSITION_MAP[data['disposition']] != data['disposition_name']:
            message = (
                'Not a consistent disposition name for the specified '
                'disposition number. Must be '
                f'{DISPOSITION_MAP[data["disposition"]]!r}.'
            )
            raise MarshmallowValidationError(message)


class Verdict(SecondaryEntity):
    schema = VerdictSchema

    def _initialize_missing_fields(self) -> None:
        self.json = {
            'type': self.type,
            **self.json
        }

    @classmethod
    def from_judgement(cls, judgement: Judgement) -> 'Verdict':
        try:
            # Make sure that `judgement` is an instance of `Judgement` before
            # extracting the actual ID out of it.
            judgement_id_field = EntityField(type=Judgement, ref=True)
            judgement_id = judgement_id_field.deserialize(judgement)
        except MarshmallowValidationError as error:
            raise BundleBuilderValidationError(*error.args) from error
        else:
            verdict = Verdict(
                disposition=judgement.disposition,
                observable=judgement.observable,
                valid_time=judgement.valid_time,
                disposition_name=judgement.disposition_name,
            )
            verdict.json['judgement_id'] = judgement_id
            return verdict