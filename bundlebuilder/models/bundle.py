from marshmallow.schema import Schema

from .entity import Entity


class BundleSchema(Schema):
    pass


class Bundle(Entity):
    schema = BundleSchema

    def generate_external_id_seed(self):
        # TODO: replace with real implementation
        return ''
