from typing import List

from marshmallow.schema import Schema

from .entity import Entity


class BundleSchema(Schema):
    pass


class Bundle(Entity):
    schema = BundleSchema

    @property
    def external_id_seed_values(self) -> List[str]:
        return [
            self.external_id_prefix,
            self.type,
        ]
