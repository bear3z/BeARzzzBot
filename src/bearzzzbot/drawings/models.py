from sqlalchemy import Boolean, Column, Integer, String

from src.bearzzzbot.models.base_class import Base


class Drawing(Base):
    id = Column(Integer, primary_key=True)
    owner = Column(String, unique=True, index=True)
    wood = Column(Boolean, default=False)
    fire = Column(Boolean, default=False)
    one = Column(Boolean, default=False)
    two = Column(Boolean, default=False)
    three = Column(Boolean, default=False)
