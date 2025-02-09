from __future__ import annotations
from typing import TYPE_CHECKING
from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from url_shortener.domain.common.models import Base

if TYPE_CHECKING:
    from url_shortener.domain.urls.models import Url


class User(Base):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(String(64), nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(128), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=False)

    urls: Mapped[list[Url]] = relationship(
        "Url", back_populates="user"
    )