from sqlalchemy import Integer, String, Boolean, Column
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    owner = Column(String, unique=True, index=True)
    wood = Column(Boolean, default=False)
    fire = Column(Boolean, default=False)
    one = Column(Boolean, default=False)
    two = Column(Boolean, default=False)
    three = Column(Boolean, default=False)