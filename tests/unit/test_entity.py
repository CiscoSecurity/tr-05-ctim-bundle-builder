from marshmallow.schema import Schema
from pytest import raises as assert_raises

from bundlebuilder.constants import (
    SCHEMA_VERSION,
    DEFAULT_SESSION_SOURCE,
    DEFAULT_SESSION_SOURCE_URI,
    DEFAULT_SESSION_EXTERNAL_ID_PREFIX,
)
from bundlebuilder.exceptions import SchemaError
from bundlebuilder.models import Entity
from bundlebuilder.session import (
    get_session,
    get_default_session,
    Session,
)
from .utils import (
    mock_id,
    mock_external_id,
)


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

        @property
        def external_id_seed_values(self):
            return []

    expected_type = 'good'

    assert get_session() == get_default_session()

    good = Good()

    assert good.json == {
        'type': good.type,
        'schema_version': good.schema_version,
        'source': good.source,
        'source_uri': good.source_uri,
        'id': good.id,
        'external_ids': good.external_ids,
    } == {
        'type': expected_type,
        'schema_version': SCHEMA_VERSION,
        'source': DEFAULT_SESSION_SOURCE,
        'source_uri': DEFAULT_SESSION_SOURCE_URI,
        'id': mock_id(DEFAULT_SESSION_EXTERNAL_ID_PREFIX, expected_type),
        'external_ids': [
            mock_external_id(DEFAULT_SESSION_EXTERNAL_ID_PREFIX, expected_type)
        ],
    }

    for index in range(10):
        session = Session(
            external_id_prefix=f'session-{index}',
            source=f'Session {index}',
            source_uri=f'https://bundlebuilder.com/session/{index}',
        )

        with session:
            assert get_session() == session
            good = Good()

        assert get_session() == get_default_session()

        assert good.json == {
            'type': expected_type,
            'schema_version': SCHEMA_VERSION,
            'source': session.source,
            'source_uri': session.source_uri,
            'id': mock_id(session.external_id_prefix, expected_type),
            'external_ids': [
                mock_external_id(session.external_id_prefix, expected_type)
            ],
        }
