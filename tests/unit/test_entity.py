from pytest import raises as assert_raises

from bundlebuilder.constants import (
    SCHEMA_VERSION,
    DEFAULT_SESSION_SOURCE,
    DEFAULT_SESSION_SOURCE_URI,
    DEFAULT_SESSION_EXTERNAL_ID_PREFIX,
)
from bundlebuilder.exceptions import SchemaError
from bundlebuilder.models.entity import (
    EntitySchema,
    BaseEntity,
    PrimaryEntity,
    SecondaryEntity,
)
from bundlebuilder.session import (
    get_session,
    get_default_session,
    Session,
)
from .utils import (
    mock_transient_id,
    mock_external_id,
)


def test_base_entity_subclassing_with_invalid_schema_fails():
    class BadSchema:
        pass

    with assert_raises(SchemaError):
        class Bad(BaseEntity):
            schema = BadSchema


def test_base_entity_abstract_subclass_instantiation_without_schema_fails():
    class AlmostGood(BaseEntity):
        def _initialize_missing_fields(self):
            pass

    with assert_raises(SchemaError):
        AlmostGood()


def test_base_entity_abstract_subclass_instantiation_without_method_fails():
    class GoodSchema(EntitySchema):
        pass

    class AlmostGood(BaseEntity):
        schema = GoodSchema

    with assert_raises(TypeError):
        AlmostGood()


def test_base_entity_subclass_validation_with_empty_schema_succeeds():
    class AlmostGood(BaseEntity):
        def _initialize_missing_fields(self):
            self.json['foo'] = 'bar'

    class GoodSchema(EntitySchema):
        pass

    class Good(AlmostGood):
        schema = GoodSchema

    good = Good()

    assert good.json == {'foo': 'bar'}


def test_primary_entity_subclass_validation_with_empty_schema_succeeds():
    class GoodSchema(EntitySchema):
        pass

    class Good(PrimaryEntity):
        schema = GoodSchema

        def generate_external_id_seed_values(self):
            yield ()

    type_ = 'good'

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
        'type': type_,
        'schema_version': SCHEMA_VERSION,
        'source': DEFAULT_SESSION_SOURCE,
        'source_uri': DEFAULT_SESSION_SOURCE_URI,
        'id': mock_transient_id(DEFAULT_SESSION_EXTERNAL_ID_PREFIX, type_),
        'external_ids': [
            mock_external_id(DEFAULT_SESSION_EXTERNAL_ID_PREFIX, type_)
        ],
    }

    for index in range(10):
        session = Session(
            external_id_prefix=f'session-{index}',
            source=f'Session {index}',
            source_uri=f'https://bundlebuilder.com/session/{index}',
        )

        with session.set():
            assert get_session() == session
            good = Good()

        assert get_session() == get_default_session()

        assert good.json == {
            'type': type_,
            'schema_version': SCHEMA_VERSION,
            'source': session.source,
            'source_uri': session.source_uri,
            'id': mock_transient_id(session.external_id_prefix, type_),
            'external_ids': [
                mock_external_id(session.external_id_prefix, type_)
            ],
        }


def test_secondary_entity_subclass_validation_with_empty_schema_succeeds():
    class GoodSchema(EntitySchema):
        pass

    class Good(SecondaryEntity):
        schema = GoodSchema

    good = Good()

    assert good.json == {}
