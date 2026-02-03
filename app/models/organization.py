from __future__ import annotations

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class Organization(Base):
    __tablename__ = "organizations"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    building_id: Mapped[int] = mapped_column(
        ForeignKey("buildings.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )

    building: Mapped["Building"] = relationship(
        "Building",
        back_populates="organizations",
    )
    phones: Mapped[list["OrganizationPhone"]] = relationship(
        "OrganizationPhone",
        back_populates="organization",
        cascade="all, delete-orphan",
    )
    activities: Mapped[list["Activity"]] = relationship(
        "Activity",
        secondary="organization_activities",
        back_populates="organizations",
    )
