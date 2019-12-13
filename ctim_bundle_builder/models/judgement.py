from marshmallow import Schema

from .entity import Entity


class JudgementSchema(Schema):
    pass


class Judgement(Entity):
    schema = JudgementSchema

    def generate_external_id_seed(self):
        # TODO: replace with real implementation
        return ''
