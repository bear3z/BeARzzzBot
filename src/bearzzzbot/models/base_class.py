import re

from sqlalchemy import MetaData
from sqlalchemy.orm import declarative_base, declared_attr

from .mixins import InspectionMixin, ReprMixin


def to_snake(s: str) -> str:
    snake_list = re.split("(?=[A-Z])", s)
    return "_".join(snake_list).lstrip("_").lower()


class GenericReprBase(InspectionMixin, ReprMixin):
    __abstract__ = True
    __name__: str

    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls) -> str:
        return f"{to_snake(cls.__name__)}s"

    # required in order to access columns with server defaults
    # or SQL expression defaults, subsequent to a flush, without
    # triggering an expired load
    __mapper_args__ = {"eager_defaults": True}


naming_convention = {
    **MetaData().naming_convention,
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "%(table_name)s_pk"
}
Base = declarative_base(
    cls=GenericReprBase, metadata=MetaData(naming_convention=naming_convention)
)
