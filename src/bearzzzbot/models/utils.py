from collections.abc import Iterable
from typing import (
    TYPE_CHECKING,
    Dict,
    List,
    Type,
    Union,
)

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from sqlalchemy.sql.schema import Table

if TYPE_CHECKING:
    from sqlalchemy.sql.elements import ClauseElement

    from .base_class import Base


def get_table(obj: Union[Table, Type["Base"], "Base"]) -> Table:
    if isinstance(obj, Table):
        return obj
    elif hasattr(obj, "__table__"):
        return obj.__table__
    return sa.inspect(obj).tables[0]


def get_columns(obj):
    return get_table(obj).columns


def get_pks(obj):
    return get_table(obj).primary_key


def table_has_column(table: Table, col: str) -> bool:
    return hasattr(table.c, col)


def build_filter_by(table: "Table", data: Dict) -> List["ClauseElement"]:
    filters = []
    for k, v in data.items():
        is_tuple =  isinstance(k, tuple)
        keys = k if is_tuple else [k]
        if not all(hasattr(table.c, key) for key in keys):
            continue
        if is_tuple:
            col = sa.tuple_(*(getattr(table.c, key) for key in keys))
        else:
            col = getattr(table.c, k)
        if (
            isinstance(v, (list, tuple))
            and len(v) == 1
            and not isinstance(col.type, (sa.ARRAY, postgresql.JSON))
            and not is_tuple
        ):
            v = v[0]
        if isinstance(v, Iterable) and not isinstance(v, str):
            if isinstance(col.type, postgresql.JSON):
                filters.append(col.contains(v))
            else:
                filters.append(col.in_(v))
        else:
            filters.append(col == v)
    return filters
