"""main tables

Revision ID: fdf8821871d7
Revises:
Create Date: 2021-10-24 01:36:44.791880

"""
from typing import Tuple

import sqlalchemy as sa
from alembic import op
from sqlalchemy import func

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


def create_customers_table() -> None:
    op.create_table(
        "customers",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column(
            "uid",
            sa.Text,
            unique=True,
            nullable=False,
            index=True,
            comment="Ex: user id: 112233445572319778929:g",
        ),
        sa.Column(
            "role_id",
            sa.Integer,
            nullable=False,
            default=0,
            index=True,
            comment="0:general, ... (TBD)",
        ),
        sa.Column(
            "provider",
            sa.Text,
            unique=False,
            nullable=False,
            index=False,
            comment="Ex: google",
        ),
        sa.Column(
            "pid",
            sa.Text,
            unique=False,
            nullable=False,
            index=True,
            comment="Ex: provider id: 112233445572319778929",
        ),
        sa.Column("username", sa.Text, nullable=True, index=True),
        sa.Column("phone", sa.Text, unique=False, nullable=True, index=True),
        sa.Column("email", sa.Text, unique=False, nullable=True, index=True),
        sa.Column("address", sa.Text, unique=False, nullable=True),
        sa.Column(
            "gender",
            sa.Integer,
            nullable=True,
            index=True,
            comment="0=None, 1=Male, 2=Female",
        ),
        sa.Column("born_year", sa.Integer, nullable=True, comment="2000"),
        sa.Column("born_month", sa.Integer, nullable=True, comment="1"),
        sa.Column("born_date", sa.Integer, nullable=True, comment="1"),
        sa.Column("occupation", sa.Text, nullable=True),
        sa.Column("bio", sa.Text, nullable=False, server_default=""),
        sa.Column("ig", sa.Text, nullable=True, comment="Instagram link"),
        sa.Column("fb", sa.Text, nullable=True, comment="Facebook link"),
        sa.Column("yt", sa.Text, nullable=True, comment="Youtube link"),
        sa.Column("image", sa.Text),
        sa.Column("cover", sa.Text),
        *timestamps(),
    )
    op.execute(
        """
        CREATE TRIGGER update_customers_modtime
            BEFORE UPDATE
            ON customers
            FOR EACH ROW
        EXECUTE PROCEDURE update_updated_at_column();
        """
    )


def create_staff_table() -> None:
    op.create_table(
        "staff",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("username", sa.Text, unique=False, nullable=False, index=True),
        sa.Column("account", sa.Text, unique=True, nullable=False, index=True),
        sa.Column("in_use", sa.Boolean, unique=False, nullable=False, index=True),
        sa.Column(
            "dpt",
            sa.Text,
            unique=False,
            nullable=True,
            index=True,
            comment="Department Ex: 化妝",
        ),
        sa.Column(
            "role",
            sa.Integer,
            unique=False,
            nullable=False,
            index=True,
            comment="0:一般 1:主管 2:super",
        ),
        sa.Column("company_name", sa.Text, unique=False, nullable=True, index=True),
        sa.Column("email", sa.Text, unique=False, nullable=True, index=True),
        sa.Column("company_seal", sa.Text, unique=False, nullable=True, index=False),
        sa.Column("boss_seal", sa.Text, unique=False, nullable=True, index=False),
        sa.Column("phone", sa.Text, unique=False, nullable=True, index=True),
        sa.Column("address", sa.Text, unique=False, nullable=True),
        sa.Column("salary", sa.Text, unique=False, nullable=True),
        sa.Column("salt", sa.Text, nullable=False),
        sa.Column("hashed_password", sa.Text),
        sa.Column("bio", sa.Text, nullable=False, server_default=""),
        sa.Column("image", sa.Text),
        *timestamps(),
    )
    op.execute(
        """
        CREATE TRIGGER update_staff_modtime
            BEFORE UPDATE
            ON staff
            FOR EACH ROW
        EXECUTE PROCEDURE update_updated_at_column();
        """
    )


def upgrade() -> None:
    create_updated_at_trigger()
    create_customers_table()
    create_staff_table()


def downgrade() -> None:
    op.drop_table("customers")
    op.drop_table("staff")
    op.execute("DROP FUNCTION update_updated_at_column")
