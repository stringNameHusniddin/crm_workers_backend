from sqlalchemy import Column, Integer, String, ForeignKey
from database import Base
from sqlalchemy.orm import relationship

class UserModel(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, index=True)
    role = Column(String)
    username = Column(String, unique=True)
    password = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)
    join_data = Column(Integer)
    age = Column(Integer)
    status = Column(String)
    boss_id = Column(Integer, default=0)

    notes = relationship("NoteModel", back_populates="owner")
    works = relationship("WorksModel", back_populates="to", foreign_keys="[WorksModel.to_id]")
    created_works = relationship("WorksModel", foreign_keys="[WorksModel.owner_id]", back_populates="owner")

class WorksModel(Base):
    __tablename__ = 'works'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    join_data = Column(Integer)
    complete_data = Column(Integer)
    status = Column(String)
    to_id = Column(Integer, ForeignKey("user.id"))
    owner_id = Column(Integer, ForeignKey("user.id"))   

    to = relationship("UserModel", back_populates="works", foreign_keys=[to_id])
    owner = relationship("UserModel", back_populates="created_works", foreign_keys=[owner_id])

class NoteModel(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True)
    text = Column(String)
    owner_id = Column(Integer, ForeignKey("user.id"))

    owner = relationship("UserModel", back_populates="notes")