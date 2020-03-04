from functools import partial
from typing import (
    Iterator,
    Tuple,
)

from marshmallow import fields
from marshmallow.decorators import validates_schema
from marshmallow.exceptions import (
    ValidationError as MarshmallowValidationError
)
from marshmallow.schema import Schema

from .entity import Entity
from .judgement import Judgement
from .utils.fields import EntityField
from .utils.schemas import (
    ObservableSchema,
    ValidTimeSchema,
)
from .utils.validators import (
    validate_integer,
    validate_string,
)
from ..constants import DISPOSITION_MAP
from ..exceptions import (
    ValidationError as BundleBuilderValidationError
)


class VerdictSchema(Schema):
    """
    https://github.com/threatgrid/ctim/blob/master/doc/structures/verdict.md
    """

    class Meta:
        ordered = True

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


class Verdict(Entity):
    schema = VerdictSchema

    def __init__(self, **data):
        super().__init__(**data)

        # Some of the default fields for CTIM don't make sense here (since
        # verdicts can't be pushed to CTIA), so just get rid of them.
        for field in (
            'schema_version',
            'source',
            'source_uri',
            'id',
            'external_ids',
        ):
            del self.json[field]

    def __str__(self):
        return f'<{self.__class__.__name__}>'

    def generate_external_id_seed_values(self) -> Iterator[Tuple[str]]:
        # Implement the abstract method somehow in order to simply make the
        # class concrete and thus instantiable.
        yield ()

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
