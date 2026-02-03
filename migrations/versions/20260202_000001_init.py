"""initial schema

Revision ID: 20260202_000001
Revises:
Create Date: 2026-02-02
"""

from alembic import op
import sqlalchemy as sa
from geoalchemy2 import Geography


# revision identifiers, used by Alembic.
revision = "20260202_000001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS postgis")

    op.create_table(
        "buildings",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("address", sa.String(length=255), nullable=False),
        sa.Column("latitude", sa.Float(), nullable=False),
        sa.Column("longitude", sa.Float(), nullable=False),
        sa.Column(
            "location",
            Geography(geometry_type="POINT", srid=4326),
            nullable=False,
        ),
    )
    op.create_index(
        "ix_buildings_location",
        "buildings",
        ["location"],
        postgresql_using="gist",
    )

    op.create_table(
        "activities",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("parent_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["parent_id"],
            ["activities.id"],
            ondelete="CASCADE",
        ),
    )
    op.create_index("ix_activities_name", "activities", ["name"])
    op.create_index("ix_activities_parent_id", "activities", ["parent_id"])

    op.create_table(
        "organizations",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("building_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["building_id"],
            ["buildings.id"],
            ondelete="RESTRICT",
        ),
    )
    op.create_index("ix_organizations_name", "organizations", ["name"])
    op.create_index("ix_organizations_building_id", "organizations", ["building_id"])

    op.create_table(
        "organization_activities",
        sa.Column("organization_id", sa.Integer(), primary_key=True),
        sa.Column("activity_id", sa.Integer(), primary_key=True),
        sa.ForeignKeyConstraint(
            ["organization_id"],
            ["organizations.id"],
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["activity_id"],
            ["activities.id"],
            ondelete="CASCADE",
        ),
    )

    op.create_table(
        "organization_phones",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("organization_id", sa.Integer(), nullable=False),
        sa.Column("phone", sa.String(length=32), nullable=False),
        sa.ForeignKeyConstraint(
            ["organization_id"],
            ["organizations.id"],
            ondelete="CASCADE",
        ),
    )
    op.create_index(
        "ix_organization_phones_organization_id",
        "organization_phones",
        ["organization_id"],
    )


def downgrade() -> None:
    op.drop_index("ix_organization_phones_organization_id", table_name="organization_phones")
    op.drop_table("organization_phones")

    op.drop_table("organization_activities")

    op.drop_index("ix_organizations_building_id", table_name="organizations")
    op.drop_index("ix_organizations_name", table_name="organizations")
    op.drop_table("organizations")

    op.drop_index("ix_activities_parent_id", table_name="activities")
    op.drop_index("ix_activities_name", table_name="activities")
    op.drop_table("activities")

    op.drop_index("ix_buildings_location", table_name="buildings")
    op.drop_table("buildings")
