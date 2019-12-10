from marshmallow import Schema

from .entity import Entity


class SightingSchema(Schema):
    pass


class Sighting(Entity):
    schema = SightingSchema
