from typing import Any, Callable, Optional, TypeVar

import orjson

from pydantic import BaseModel

Schema = TypeVar("Schema", bound=BaseModel)


def orjson_dumps(v: Any, *, default: Optional[Callable[[Any], Any]] = None) -> str:
    """
    orjson.dumps returns bytes, to match standard json.dumps we need to decode.
    orjson.dumps option arguments provide many options such as `option=orjson.
        OPT_SERIALIZE_UUID` to natively encode UUID instances.
    """
    return orjson.dumps(v, default=default).decode()


class SchemaBase(BaseModel):
    class Config:
        orm_mode = True
        validate_assignment = True
        allow_population_by_field_name = True
        json_loads = orjson.loads
        json_dumps = orjson_dumps
