from marshmallow import Schema

from .entity import Entity


class SightingSchema(Schema):
    pass


class Sighting(Entity):
    schema = SightingSchema

    def generate_external_id_seed(self):
        # TODO: replace with real implementation
        return ''
