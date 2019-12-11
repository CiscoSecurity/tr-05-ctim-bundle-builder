from marshmallow import Schema

from .entity import Entity


class JudgementSchema(Schema):
    pass


class Judgement(Entity):
    schema = JudgementSchema

    @property
    def summary(self):
        # TODO: replace with real implementation
        return ''
