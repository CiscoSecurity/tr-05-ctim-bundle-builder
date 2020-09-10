from marshmallow.decorators import post_load

from ..entity import (
    EntitySchema,
    SecondaryEntity,
)
from ..fields import StringField
from ..validators import validate_string


class KillChainPhaseSchema(EntitySchema):
    kill_chain_name = StringField(
        validate=validate_string,
        required=True,
    )
    phase_name = StringField(
        validate=validate_string,
        required=True,
    )

    @post_load
    def normalize_names(self, data, **kwargs):
        for field in ('kill_chain_name', 'phase_name'):
            if field in data:
                data[field] = '-'.join(
                    data[field].replace('_', ' ').replace('-', ' ').split()
                ).lower()
        return data


class KillChainPhase(SecondaryEntity):
    schema = KillChainPhaseSchema
