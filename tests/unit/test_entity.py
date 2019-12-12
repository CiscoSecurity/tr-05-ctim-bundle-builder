from marshmallow import Schema
from pytest import raises as assert_raises

from ctim_bundle_builder.exceptions import SchemaError
from ctim_bundle_builder.models import Entity
from .utils import mock_id, mock_external_id


def test_subclassing_without_marshmallow_schema_fails():
    class BadSchema:
        pass

    with assert_raises(SchemaError):
        class Bad(Entity):
            schema = BadSchema


def test_abstract_subclass_instantiation_fails():
    class AlmostGoodSchema(Schema):
        pass

    class AlmostGood(Entity):
        schema = AlmostGoodSchema

    with assert_raises(TypeError):
        AlmostGood()


def test_empty_schema_validation_succeeds():
    class GoodSchema(Schema):
        pass

    class Good(Entity):
        schema = GoodSchema

        def generate_external_id_seed(self):
            return 'mock'

    good = Good()

    assert good.json == {
        'type': good.type,
        'id': good.id,
        'external_ids': good.external_ids,
    } == {
        'type': 'good',
        'id': mock_id('good'),
        'external_ids': [mock_external_id('good')],
    }
