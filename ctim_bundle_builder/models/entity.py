import abc
import hashlib

from marshmallow.schema import Schema

from ..constants import EXTERNAL_ID_PREFIX
from ..exceptions import SchemaError


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
        self.json = self.schema().load(data)

        self.json['type'] = self.type

        self.json.setdefault('id', self.generate_id())

        self.json.setdefault('external_ids', []).append(
            self.generate_external_id()
        )

    def __getattr__(self, field):
        return self.json.get(field)

    def generate_id(self):
        return 'transient:' + self.generate_external_id()

    def generate_external_id(self):
        return '{prefix}-{entity_type}-{sha256_hash}'.format(
            prefix=EXTERNAL_ID_PREFIX,
            entity_type=self.type,
            sha256_hash=hashlib.sha256(
                bytes(self.generate_external_id_seed(), 'utf-8')
            ).hexdigest(),
        )

    @abc.abstractmethod
    def generate_external_id_seed(self):
        """Return a deterministic string based on some fields of the entity."""
