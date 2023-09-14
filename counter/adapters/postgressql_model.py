from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class ObjectCountEntity(Base):
    __tablename__ = 'object_counts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    object_class = Column(String, nullable=False)
    count = Column(Integer, nullable=False)