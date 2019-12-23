from marshmallow import Schema

from .entity import Entity


class IndicatorSchema(Schema):
    pass


class Indicator(Entity):
    schema = IndicatorSchema

    def generate_external_id_seed(self):
        # TODO: replace with real implementation
        return ''
