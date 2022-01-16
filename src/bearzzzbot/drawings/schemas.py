from src.bearzzzbot.schemas import SchemaBase


class DrawingBase(SchemaBase):
    owner: str
    wood: bool
    fire: bool
    one: bool
    two: bool
    three: bool


class DrawingCreate(DrawingBase):
    ...


class DrawingCreateIn(DrawingBase):
    ...
