"""main tables

Revision ID: fdf8821871d7
Revises:
Create Date: 2022-04-10 01:36:44.791880

"""
from typing import Tuple

import sqlalchemy as sa
from alembic import op
from sqlalchemy import func
from sqlalchemy.dialects.postgresql import JSONB

revision = "fdf8821871d7"
down_revision = None
branch_labels = None
depends_on = None


def create_updated_at_trigger() -> None:
    op.execute(
        """
    CREATE FUNCTION update_updated_at_column()
        RETURNS TRIGGER AS
    $$
    BEGIN
        NEW.updated_at = now();
        RETURN NEW;
    END;
    $$ language 'plpgsql';
    """
    )


def timestamps() -> Tuple[sa.Column, sa.Column]:
    return (
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=func.now(),
        ),
        sa.Column(
            "updated_at",
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=func.now(),
        ),
    )


def create_stores_table() -> None:
    op.create_table(
        "stores",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column(
            "name",
            sa.Text,
            unique=False,
            nullable=False,
            index=False,
            comment="Ex: 鷹流拉麵中山店",
        ),
        sa.Column(
            "phone", sa.Text, nullable=True, index=False, comment="Ex: 0912345678"
        ),
        sa.Column(
            "address", sa.Text, nullable=True, index=False, comment="Ex: 台北市中山區中山北路二段"
        ),
        sa.Column("rating", sa.Float, nullable=True, index=False, comment="Ex: 4.5"),
        sa.Column(
            "review_count", sa.Integer, nullable=True, index=False, comment="Ex: 150"
        ),
        sa.Column(
            "image",
            JSONB,
            unique=False,
            nullable=True,
            index=False,
            comment="Ex:{'style': 'cover', 'url': 'http://oo.jpeg', 'width': '1024', 'height': '768', 'content_type': 'image/jpg'}",
        ),
        sa.Column(
            "social_media",
            JSONB,
            unique=False,
            nullable=True,
            index=False,
            comment="Ex:{'facebook': 'xxxx', 'ig': 'xxxx'}",
        ),
        sa.Column(
            "business_hours",
            JSONB,
            unique=False,
            nullable=True,
            index=False,
            comment="Ex:{'mo': '星期一 11:00-14:00 17:00-23:00', 'tu': '星期二 11:00-14:00 17:00-23:00'}",
        ),
        sa.Column(
            "status",
            sa.Integer,
            nullable=False,
            index=True,
            comment="Ex: 0: 草稿, 1: 已發佈, 2: 已刪除",
        ),
        *timestamps(),
    )
    op.execute(
        """
        CREATE TRIGGER update_stores_modtime
            BEFORE UPDATE
            ON stores
            FOR EACH ROW
        EXECUTE PROCEDURE update_updated_at_column();
        """
    )


def upgrade() -> None:
    create_updated_at_trigger()
    create_stores_table()


def downgrade() -> None:
    op.drop_table("stores")
    op.execute("DROP FUNCTION update_updated_at_column")
