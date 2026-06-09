"""initial schema

Revision ID: 0001_initial
Revises:
Create Date: 2026-06-06
"""

from alembic import op
import sqlalchemy as sa

revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "inventory",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("total_gadda", sa.Integer(), nullable=False),
        sa.Column("available_gadda", sa.Integer(), nullable=False),
        sa.Column("total_rajai", sa.Integer(), nullable=False),
        sa.Column("available_rajai", sa.Integer(), nullable=False),
        sa.Column("deposit_per_item", sa.Integer(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "visitors",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("issue_id", sa.String(length=20), nullable=False),
        sa.Column("full_name", sa.String(length=120), nullable=False),
        sa.Column("mobile", sa.String(length=15), nullable=False),
        sa.Column("stay_days", sa.Integer(), nullable=False),
        sa.Column("gadda_qty", sa.Integer(), nullable=False),
        sa.Column("rajai_qty", sa.Integer(), nullable=False),
        sa.Column("deposit_amount", sa.Integer(), nullable=False),
        sa.Column("issue_datetime", sa.DateTime(timezone=True), nullable=False),
        sa.Column("return_datetime", sa.DateTime(timezone=True), nullable=True),
        sa.Column("status", sa.String(length=12), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("issue_id"),
    )
    op.create_index(op.f("ix_visitors_issue_id"), "visitors", ["issue_id"], unique=False)
    op.create_index(op.f("ix_visitors_mobile"), "visitors", ["mobile"], unique=False)
    op.create_index(op.f("ix_visitors_status"), "visitors", ["status"], unique=False)


def downgrade():
    op.drop_index(op.f("ix_visitors_status"), table_name="visitors")
    op.drop_index(op.f("ix_visitors_mobile"), table_name="visitors")
    op.drop_index(op.f("ix_visitors_issue_id"), table_name="visitors")
    op.drop_table("visitors")
    op.drop_table("inventory")
