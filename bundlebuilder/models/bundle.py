from typing import List

from marshmallow.schema import Schema

from .entity import Entity


class BundleSchema(Schema):
    pass


class Bundle(Entity):
    schema = BundleSchema

    @property
    def external_id_core_values(self) -> List[str]:
        # TODO: replace with real implementation
        return []
