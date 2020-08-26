from abc import (
    ABCMeta,
    abstractmethod,
)
from hashlib import sha256
from inspect import (
    Signature,
    Parameter,
)
from itertools import chain
from typing import (
    Optional,
    Any,
    List,
    Iterator,
    Tuple,
)
from uuid import uuid4

from inflection import underscore
from marshmallow.exceptions import (
    ValidationError as MarshmallowValidationError
)
from marshmallow.schema import Schema

from ..constants import SCHEMA_VERSION
from ..exceptions import (
    SchemaError,
    ValidationError as BundleBuilderValidationError,
)


class EntitySchema(Schema):

    class Meta:
        ordered = True


class EntityMeta(ABCMeta):

    def __init__(cls, cls_name, cls_bases, cls_dict):
        cls_type = cls_dict.get('type')
        if cls_type is None:
            cls.type = underscore(cls.__name__)  # CamelCase -> snake_case

        cls_schema = cls_dict.get('schema')

        if cls_schema is None:
            # If there is no schema then make the class kind of abstract by not
            # allowing to instantiate it although allowing inheritance from it.

            def schema(self):
                raise SchemaError(
                    f'{cls}.schema must be a subclass of {EntitySchema}.'
                )

            cls.schema = schema

            super().__init__(cls_name, cls_bases, cls_dict)
            return

        if not (
            isinstance(cls_schema, type) and
            issubclass(cls_schema, EntitySchema)
        ):
            raise SchemaError(
                f'{cls}.schema must be a subclass of {EntitySchema}.'
            )

        cls.__signature__ = Signature([
            Parameter(name, Parameter.KEYWORD_ONLY)
            for name in cls_schema().declared_fields.keys()
        ])

        super().__init__(cls_name, cls_bases, cls_dict)


class BaseEntity(metaclass=EntityMeta):

    def __init__(self, **data):
        try:
            self.json = self.schema().load(data)
        except MarshmallowValidationError as error:
            raise BundleBuilderValidationError(*error.args) from error

        self._initialize_missing_fields()

    def __getattr__(self, field) -> Optional[Any]:
        return self.json.get(field)

    @abstractmethod
    def _initialize_missing_fields(self) -> None:
        pass


class PrimaryEntity(BaseEntity):

    def _initialize_missing_fields(self) -> None:
        self.json['type'] = self.type

        self.json['schema_version'] = SCHEMA_VERSION

        # Use a dynamic import to break the circular dependency.
        from ..session import get_session

        session = get_session()

        self.external_id_prefix = session.external_id_prefix

        self.json.setdefault('source', session.source)
        self.json.setdefault('source_uri', session.source_uri)

        # This isn't really a part of the CTIM JSON payload, so extract it out.
        self.external_id_salt_values: List[str] = sorted(
            self.json.pop('external_id_salt_values', [])
        )

        # Generate and set a transient ID and a list of XIDs only after all the
        # other attributes are already set properly.
        self.json['id'] = self.generate_transient_id()
        self.json['external_ids'] = (
            self.generate_external_ids() + self.json.get('external_ids', [])
        )

        # Make the automatically populated fields be listed before the ones
        # manually specified by the user.
        self.json = {
            'type': self.json.pop('type'),
            'schema_version': self.json.pop('schema_version'),
            'source': self.json.pop('source'),
            'source_uri': self.json.pop('source_uri'),
            'id': self.json.pop('id'),
            'external_ids': self.json.pop('external_ids'),
            **self.json
        }

    def generate_transient_id(self) -> str:
        return 'transient:{prefix}-{type}-{uuid}'.format(
            prefix=self.external_id_prefix,
            type=self.type,
            uuid=uuid4().hex,
        )

    def generate_external_ids(self) -> List[str]:
        return [
            '{prefix}-{type}-{sha256}'.format(
                prefix=self.external_id_prefix,
                type=self.type,
                sha256=sha256(
                    bytes(external_id_deterministic_value, 'utf-8')
                ).hexdigest(),
            )
            for external_id_deterministic_value
            in self.generate_external_id_deterministic_values()
        ]

    def generate_external_id_deterministic_values(self) -> Iterator[str]:
        for external_id_seed_values in self.generate_external_id_seed_values():
            # Chain together all the values available.
            # Filter out any empty values.
            # Join up all the values left.
            yield '|'.join(
                filter(
                    bool,
                    chain(
                        external_id_seed_values,
                        self.external_id_salt_values,
                    )
                )
            )

    @abstractmethod
    def generate_external_id_seed_values(self) -> Iterator[Tuple[str]]:
        pass


class SecondaryEntity(BaseEntity):

    def _initialize_missing_fields(self) -> None:
        pass
