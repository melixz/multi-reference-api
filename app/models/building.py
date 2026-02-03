from __future__ import annotations

from geoalchemy2 import Geography
from sqlalchemy import Float, Index, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class Building(Base):
    __tablename__ = "buildings"

    id: Mapped[int] = mapped_column(primary_key=True)
    address: Mapped[str] = mapped_column(String(255), nullable=False)
    latitude: Mapped[float] = mapped_column(Float, nullable=False)
    longitude: Mapped[float] = mapped_column(Float, nullable=False)
    location: Mapped[object] = mapped_column(
        Geography(geometry_type="POINT", srid=4326),
        nullable=False,
    )

    organizations: Mapped[list["Organization"]] = relationship(
        "Organization",
        back_populates="building",
        cascade="all, delete-orphan",
    )

    __table_args__ = (Index("ix_buildings_location", "location", postgresql_using="gist"),)
