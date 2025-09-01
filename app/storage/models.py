from __future__ import annotations

from datetime import datetime
from typing import Optional, List

from sqlalchemy import BigInteger, Boolean, DateTime, Enum, ForeignKey, JSON, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from app.utils.enums import Channel, ListingStatus, ListingType, Role


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[int] = mapped_column(BigInteger, unique=True, index=True)
    role: Mapped[Role] = mapped_column(Enum(Role), default=Role.unknown)
    name: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    contact: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    location: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
    is_banned: Mapped[bool] = mapped_column(Boolean, default=False)

    listings: Mapped[List["Listing"]] = relationship(back_populates="author")


class Listing(Base):
    __tablename__ = "listings"

    id: Mapped[int] = mapped_column(primary_key=True)
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    type: Mapped[ListingType] = mapped_column(Enum(ListingType))
    title: Mapped[str] = mapped_column(Text)
    description: Mapped[str] = mapped_column(Text)
    skills: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    pay: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    location: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    deadline: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    status: Mapped[ListingStatus] = mapped_column(Enum(ListingStatus), default=ListingStatus.draft)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)

    author: Mapped[User] = relationship(back_populates="listings")
    channel_post: Mapped["ChannelPost"] = relationship(back_populates="listing", uselist=False)


class ChannelPost(Base):
    __tablename__ = "channel_posts"

    id: Mapped[int] = mapped_column(primary_key=True)
    listing_id: Mapped[int] = mapped_column(ForeignKey("listings.id"))
    channel: Mapped[Channel] = mapped_column(Enum(Channel))
    message_id: Mapped[int] = mapped_column(BigInteger)
    posted_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)

    listing: Mapped[Listing] = relationship(back_populates="channel_post")


class Setting(Base):
    __tablename__ = "settings"

    key: Mapped[str] = mapped_column(Text, primary_key=True)
    value: Mapped[dict] = mapped_column(JSON)
