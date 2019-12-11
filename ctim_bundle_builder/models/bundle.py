from marshmallow import Schema

from .entity import Entity


class BundleSchema(Schema):
    pass


class Bundle(Entity):
    schema = BundleSchema
