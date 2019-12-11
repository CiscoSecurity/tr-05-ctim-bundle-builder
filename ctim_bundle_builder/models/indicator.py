from marshmallow import Schema

from .entity import Entity


class IndicatorSchema(Schema):
    pass


class Indicator(Entity):
    schema = IndicatorSchema

    @property
    def summary(self):
        # TODO: replace with real implementation
        return ''
