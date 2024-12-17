from sqlalchemy import Column, Integer, String, Boolean, DateTime
import datetime
from configdb import Base,engine

class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    completed = Column(Boolean, default=False)
    date = Column(DateTime, default=datetime.datetime.utcnow)

# Crear la tabla si no existe
Base.metadata.create_all(bind=engine)