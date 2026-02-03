from __future__ import annotations

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class Activity(Base):
    __tablename__ = "activities"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    parent_id: Mapped[int | None] = mapped_column(
        ForeignKey("activities.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )

    parent: Mapped["Activity | None"] = relationship(
        "Activity",
        remote_side="Activity.id",
        back_populates="children",
    )
    children: Mapped[list["Activity"]] = relationship(
        "Activity",
        back_populates="parent",
        cascade="all, delete-orphan",
    )

    organizations: Mapped[list["Organization"]] = relationship(
        "Organization",
        secondary="organization_activities",
        back_populates="activities",
    )
