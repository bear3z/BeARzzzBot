from typing import List, Optional

import sqlalchemy as sa
from sqlalchemy.ext.hybrid import hybrid_method, hybrid_property
from sqlalchemy.orm.relationships import RelationshipProperty
from sqlalchemy.util.langhelpers import symbol

from .utils import get_columns

NO_VALUE = symbol("NO_VALUE")
NOT_LOADED_REPR = "<not loaded>"


class ReprMixin:
    __abstract__ = True
    __repr_fields__: Optional[List] = None
    __repr_max_fields__: Optional[int] = None

    def __repr__(self):
        state = sa.inspect(self)
        if not self.__repr_fields__:
            fields = state.mapper.columns.keys()[: self.__repr_max_fields__]
        else:
            fields = self.__repr_fields__

        field_reprs = []
        for key in fields:
            value = state.attrs[key].loaded_value
            if value == NO_VALUE:
                value = NOT_LOADED_REPR
            else:
                value = repr(value)
            field_reprs.append(f"{key}={value}")

        return f'{type(self).__name__}({", ".join(field_reprs)})'


class classproperty:
    def __init__(self, getter):
        self.getter = getter

    def __get__(self, instance, owner):
        return self.getter(owner)


# modified from sqlalchemy_mixins
#   See: https://github.com/absent1706/sqlalchemy-mixins/blob/master/sqlalchemy_mixins/inspection.py
class InspectionMixin:  # pragma: no cover
    __abstract__ = True

    @classproperty
    def columns(cls):
        return get_columns(cls)

    @classproperty
    def column_keys(cls):
        return cls.columns.keys()

    @classproperty
    def primary_keys_full(cls):
        """Get primary key properties for a SQLAlchemy cls.
        Taken from marshmallow_sqlalchemy
        """
        mapper = cls.__mapper__  # type: ignore
        return [mapper.get_property_by_column(column) for column in mapper.primary_key]

    @classproperty
    def primary_keys(cls):
        return [pk.key for pk in cls.primary_keys_full]

    @classproperty
    def relations(cls):
        """Return a `list` of relationship names or the given model"""
        return [
            c.key
            for c in cls.__mapper__.iterate_properties  # type: ignore
            if isinstance(c, RelationshipProperty)
        ]

    @classproperty
    def settable_relations(cls):
        """Return a `list` of relationship names or the given model"""
        return [r for r in cls.relations if getattr(cls, r).property.viewonly is False]

    @classproperty
    def hybrid_properties(cls):
        items = sa.inspect(cls).all_orm_descriptors
        return [item.__name__ for item in items if type(item) == hybrid_property]

    @classproperty
    def hybrid_methods_full(cls):
        items = sa.inspect(cls).all_orm_descriptors
        return {
            item.func.__name__: item for item in items if type(item) == hybrid_method
        }

    @classproperty
    def hybrid_methods(cls):
        return list(cls.hybrid_methods_full.keys())
