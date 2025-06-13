from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlalchemy import (Boolean, Column, DateTime, ForeignKey, Integer, String,
                        create_engine, func)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Mapped, relationship, sessionmaker

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = Column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[str] = Column(String, unique=True, nullable=False)
    name: Mapped[str] = Column(String, nullable=False)
    handle: Mapped[str] = Column(String, nullable=False)
    description: Mapped[Optional[str]] = Column(String)
    created_at: Mapped[Optional[datetime]] = Column(DateTime)
    last_checked_at: Mapped[Optional[datetime]] = Column(DateTime)

    tweets: Mapped[list["Tweet"]] = relationship("Tweet", back_populates="user")


class Tweet(Base):
    __tablename__ = "tweets"

    id: Mapped[int] = Column(Integer, primary_key=True, autoincrement=True)
    tweet_id: Mapped[str] = Column(String, unique=True, nullable=False)
    user_id: Mapped[int] = Column(Integer, ForeignKey("users.id"), nullable=False)
    text: Mapped[str] = Column(String, nullable=False)
    tweet_created_at: Mapped[datetime] = Column(DateTime, nullable=False)
    fetched_at: Mapped[datetime] = Column(DateTime, default=func.now())

    user: Mapped["User"] = relationship("User", back_populates="tweets")


def get_engine(db_path: str = "sqlite:///fin_tweet.db"):
    return create_engine(db_path, connect_args={"check_same_thread": False})


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=get_engine())


def init_db(engine=None) -> None:
    if engine is None:
        engine = get_engine()
    Base.metadata.create_all(bind=engine)
