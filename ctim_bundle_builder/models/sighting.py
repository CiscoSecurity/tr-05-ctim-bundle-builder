from marshmallow import Schema

from .entity import Entity


class SightingSchema(Schema):
    pass


class Sighting(Entity):
    schema = SightingSchema

    @property
    def summary(self):
        # TODO: replace with real implementation
        return ''
