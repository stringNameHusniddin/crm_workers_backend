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
    join_data = Column(String)
    age = Column(Integer)
    status = Column(String)
    boss_id = Column(Integer, default=0)

    notes = relationship("NoteModel", back_populates="owner")
    works = relationship("WorksModel", back_populates="to", foreign_keys="[WorksModel.to_id]")
    created_works = relationship("WorksModel", foreign_keys="[WorksModel.owner_id]", back_populates="owner")
    notifications = relationship("Notification", foreign_keys="[Notification.to_id]", back_populates="to")
    created_notifications = relationship("Notification", foreign_keys="[Notification.owner_id]", back_populates="owner")

class WorksModel(Base):
    __tablename__ = 'works'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    join_data = Column(String)
    complete_data = Column(String)
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

class Notification(Base):
    __tablename__ = "notification"

    id = Column(Integer, primary_key=True)
    text = Column(String)
    owner_id = Column(Integer, ForeignKey("user.id"))
    to_id = Column(Integer, ForeignKey("user.id"))

    to = relationship("UserModel", back_populates="notifications", foreign_keys=[to_id])
    owner = relationship("UserModel", back_populates="created_notifications", foreign_keys=[owner_id])