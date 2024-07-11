from sqlalchemy import Column, Integer, Text, Boolean
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "discord_user"
    discord_id = Column(Integer, nullable=False, primary_key=True)
    user_id = Column(Text, nullable=False)
    activated = Column(Boolean, nullable=False, default=True)
    id = Column(Integer, nullable=False, autoincrement=True)


class Whitelist(Base):
    __tablename__ = "whitelist"
    user_id = Column(Text, nullable=False, primary_key=True)

class Player(Base):
    __tablename__ = "player"
    player_id = Column(Integer, nullable=False, primary_key=True)
    user_id = Column(Text, nullable=False)
    last_seen_user_name = Column(Text, nullable=False)
