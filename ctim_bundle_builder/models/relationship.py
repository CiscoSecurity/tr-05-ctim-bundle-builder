from marshmallow import Schema

from .entity import Entity


class RelationshipSchema(Schema):
    pass


class Relationship(Entity):
    schema = RelationshipSchema
