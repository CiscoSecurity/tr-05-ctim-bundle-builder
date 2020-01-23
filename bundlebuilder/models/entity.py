import abc
import hashlib
from itertools import chain
from typing import List

from marshmallow.exceptions import (
    ValidationError as MarshmallowValidationError
)
from marshmallow.schema import Schema

from ..constants import SCHEMA_VERSION
from ..exceptions import (
    SchemaError,
    ValidationError as BundleBuilderValidationError,
)


class EntityMeta(abc.ABCMeta):

    def __init__(cls, cls_name, cls_bases, cls_dict):
        cls_schema = cls_dict.get('schema')
        if not (
            isinstance(cls_schema, type) and issubclass(cls_schema, Schema)
        ):
            raise SchemaError(
                '{}.schema must be a subclass of {} instead of {}.'.format(
                    cls, Schema, cls_schema
                )
            )

        cls_type = cls_dict.get('type')
        if cls_type is None:
            cls.type = cls.__name__.lower()

        super().__init__(cls_name, cls_bases, cls_dict)


class EntitySchema(Schema):
    pass


class Entity(metaclass=EntityMeta):
    schema = EntitySchema

    def __init__(self, **data):
        try:
            self.json = self.schema().load(data)
        except MarshmallowValidationError as error:
            raise BundleBuilderValidationError(data=error.messages) from error

        self.json['type'] = self.type

        self.json['schema_version'] = SCHEMA_VERSION

        # Use a dynamic import to break the circular dependency.
        from ..session import get_session

        session = get_session()

        self.external_id_prefix = session.external_id_prefix

        # This isn't really a part of the CTIM JSON payload, so extract it out.
        self.external_id_extra_values: List[str] = sorted(
            self.json.pop('external_id_extra_values', [])
        )

        self.json['source'] = session.source
        self.json['source_uri'] = session.source_uri

        # Generate and set a transient ID and an XID only after
        # all the other attributes are already set properly.
        self.json['id'] = self.generate_id()
        self.json['external_ids'] = [self.generate_external_id()]

    def __getattr__(self, field):
        return self.json.get(field)

    def generate_id(self) -> str:
        return 'transient:' + self.generate_external_id()

    def generate_external_id(self) -> str:
        return '{prefix}-{type}-{sha256}'.format(
            prefix=self.external_id_prefix,
            type=self.type,
            sha256=hashlib.sha256(
                bytes(self.external_id_deterministic_value, 'utf-8')
            ).hexdigest(),
        )

    @property
    def external_id_deterministic_value(self) -> str:
        return '|'.join(
            chain(self.external_id_seed_values, self.external_id_extra_values)
        )

    @property
    @abc.abstractmethod
    def external_id_seed_values(self) -> List[str]:
        pass
