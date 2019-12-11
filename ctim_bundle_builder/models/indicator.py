from marshmallow import Schema

from .entity import Entity


class IndicatorSchema(Schema):
    pass


class Indicator(Entity):
    schema = IndicatorSchema
