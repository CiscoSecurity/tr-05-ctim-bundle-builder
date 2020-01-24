from typing import (
    Iterator,
    Tuple,
)

from marshmallow.schema import Schema

from .entity import Entity


class BundleSchema(Schema):
    pass


class Bundle(Entity):
    schema = BundleSchema

    def generate_external_id_seed_values(self) -> Iterator[Tuple[str]]:
        yield (
            self.external_id_prefix,
            self.type,
        )
