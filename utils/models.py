from sqlalchemy import Column, Integer, Text
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "user"
    discord_id = Column(Integer, nullable=False, primary_key=True)
    user_id = Column(Text, nullable=False)


class Whitelist(Base):
    __tablename__ = "whitelist"
    discord_id = Column(Integer, nullable=False, primary_key=True)
    user_id = Column(Text, nullable=False)
