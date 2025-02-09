from __future__ import annotations

from uuid import UUID
from sqlalchemy import ForeignKey, String, Text, Integer
from sqlalchemy.orm import relationship, Mapped, mapped_column

from url_shortener.domain.common.models import Base
from url_shortener.domain.auth.models import User


class Url(Base):
    __tablename__ = "urls"

    original_url: Mapped[str] = mapped_column(String(256), nullable=False)
    shortened_url: Mapped[str] = mapped_column(String(32), nullable=True)

    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    user: Mapped[User] = relationship("User", back_populates="urls")
