from functools import partial
from typing import (
    Iterator,
    Tuple,
)

from marshmallow import fields
from marshmallow.exceptions import (
    ValidationError as MarshmallowValidationError
)

from ..fields import (
    EntityField,
    DateTimeField,
)
from ..entity import (
    EntitySchema,
    PrimaryEntity,
)
from ..primary.indicator import Indicator
from ..primary.judgement import Judgement
from ..primary.relationship import Relationship
from ..primary.sighting import Sighting
from ..primary.verdict import Verdict
from ..secondary.external_reference import ExternalReference
from ..schemas import ValidTimeSchema
from ..validators import (
    validate_string,
    validate_integer,
)
from ...constants import (
    SOURCE_MAX_LENGTH,
    DESCRIPTION_MAX_LENGTH,
    LANGUAGE_MAX_LENGTH,
    REVISION_MIN_VALUE,
    SHORT_DESCRIPTION_LENGTH,
    TITLE_MAX_LENGTH,
    TLP_CHOICES,
)
from ...exceptions import (
    ValidationError as BundleBuilderValidationError
)


class BundleSchema(EntitySchema):
    """
    https://github.com/threatgrid/ctim/blob/master/doc/structures/bundle.md
    """

    valid_time = fields.Nested(ValidTimeSchema)
    description = fields.String(
        validate=partial(validate_string, max_length=DESCRIPTION_MAX_LENGTH),
    )
    external_references = fields.List(
        EntityField(type=ExternalReference)
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
    verdict_refs = fields.List(
        EntityField(type=Verdict, ref=True)
    )
    verdicts = fields.List(
        EntityField(type=Verdict)
    )

    source = fields.String(
        validate=partial(validate_string, max_length=SOURCE_MAX_LENGTH),
    )
    source_uri = fields.String(
        validate=validate_string,
    )

    external_id_salt_values = fields.List(
        fields.String(
            validate=validate_string,
        )
    )
    external_ids = fields.List(
        fields.String(
            validate=validate_string,
        )
    )


class Bundle(PrimaryEntity):
    schema = BundleSchema

    def add_indicator(self, indicator: Indicator, ref: bool = False) -> None:
        self._add(indicator, Indicator, ref)

    def add_judgement(self, judgement: Judgement, ref: bool = False) -> None:
        self._add(judgement, Judgement, ref)

    def add_relationship(self, relationship: Relationship, ref: bool = False) -> None:  # noqa: E501
        self._add(relationship, Relationship, ref)

    def add_sighting(self, sighting: Sighting, ref: bool = False) -> None:
        self._add(sighting, Sighting, ref)

    def add_verdict(self, verdict: Verdict, ref: bool = False) -> None:
        self._add(verdict, Verdict, ref)

    def _add(self, entity, type_, ref):
        try:
            field = EntityField(type=type_, ref=ref)
            data = field.deserialize(entity)
        except MarshmallowValidationError as error:
            raise BundleBuilderValidationError(*error.args) from error
        else:
            key = type_.type + ('_refs' if ref else 's')
            self.json.setdefault(key, []).append(data)

    def _generate_external_id_seed_values(self) -> Iterator[Tuple[str]]:
        yield (
            self.type,
        )
