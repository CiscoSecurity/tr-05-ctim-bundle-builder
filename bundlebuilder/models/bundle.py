from functools import partial
from typing import (
    Iterator,
    Tuple,
)

from marshmallow import fields
from marshmallow.exceptions import (
    ValidationError as MarshmallowValidationError
)
from marshmallow.schema import Schema

from .entity import Entity
from .indicator import Indicator
from .judgement import Judgement
from .relationship import Relationship
from .sighting import Sighting
from .utils.fields import (
    EntityField,
    DateTimeField,
)
from .utils.schemas import (
    ValidTimeSchema,
    ExternalReferenceSchema,
)
from .utils.validators import (
    validate_string,
    validate_integer,
)
from ..constants import (
    DESCRIPTION_MAX_LENGTH,
    LANGUAGE_MAX_LENGTH,
    REVISION_MIN_VALUE,
    SHORT_DESCRIPTION_LENGTH,
    TITLE_MAX_LENGTH,
    TLP_CHOICES,
)
from ..exceptions import (
    ValidationError as BundleBuilderValidationError
)


class BundleSchema(Schema):
    """
    https://github.com/threatgrid/ctim/blob/master/doc/structures/bundle.md
    """
    valid_time = fields.Nested(
        ValidTimeSchema,
        required=True,
    )
    description = fields.String(
        validate=partial(validate_string, max_length=DESCRIPTION_MAX_LENGTH),
    )
    external_references = fields.List(
        fields.Nested(ExternalReferenceSchema)
    )
    indicator_refs = fields.List(
        EntityField(type=Indicator, ref=True)
    )
    indicators = fields.List(
        EntityField(type=Indicator)
    )
    judgement_refs = fields.List(
        EntityField(type=Judgement, ref=True)
    )
    judgements = fields.List(
        EntityField(type=Judgement)
    )
    language = fields.String(
        validate=partial(validate_string, max_length=LANGUAGE_MAX_LENGTH),
    )
    relationship_refs = fields.List(
        EntityField(type=Relationship, ref=True)
    )
    relationships = fields.List(
        EntityField(type=Relationship)
    )
    revision = fields.Integer(
        validate=partial(validate_integer, min_value=REVISION_MIN_VALUE),
    )
    short_description = fields.String(
        validate=partial(validate_string, max_length=SHORT_DESCRIPTION_LENGTH),
    )
    sighting_refs = fields.List(
        EntityField(type=Sighting, ref=True)
    )
    sightings = fields.List(
        EntityField(type=Sighting)
    )
    timestamp = DateTimeField()
    title = fields.String(
        validate=partial(validate_string, max_length=TITLE_MAX_LENGTH),
    )
    tlp = fields.String(
        validate=partial(validate_string, choices=TLP_CHOICES),
    )

    external_id_salt_values = fields.List(
        fields.String(
            validate=validate_string,
        )
    )


class Bundle(Entity):
    schema = BundleSchema

    def generate_external_id_seed_values(self) -> Iterator[Tuple[str]]:
        yield (
            self.external_id_prefix,
            self.type,
        )

    def _adder(self, type_, ref):
        field = EntityField(type=type_, ref=ref)

        def add(entity):
            try:
                data = field.deserialize(entity)
            except MarshmallowValidationError as error:
                raise BundleBuilderValidationError(*error.args) from error
            else:
                key = type_.type + ('_refs' if ref else 's')
                self.json.setdefault(key, []).append(data)

        return add

    def add_indicator(self, indicator: Indicator, ref: bool = False):
        self._adder(Indicator, ref)(indicator)

    def add_judgement(self, judgement: Judgement, ref: bool = False):
        self._adder(Judgement, ref)(judgement)

    def add_relationship(self, relationship: Relationship, ref: bool = False):
        self._adder(Relationship, ref)(relationship)

    def add_sighting(self, sighting: Sighting, ref: bool = False):
        self._adder(Sighting, ref)(sighting)
