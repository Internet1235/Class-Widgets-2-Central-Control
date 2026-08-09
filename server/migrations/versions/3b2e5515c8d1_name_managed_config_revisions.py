"""name managed config revisions

Revision ID: 3b2e5515c8d1
Revises: ddf7460703a8
Create Date: 2026-08-09
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "3b2e5515c8d1"
down_revision: str | Sequence[str] | None = "ddf7460703a8"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "policy_revisions",
        sa.Column("name", sa.String(length=120), nullable=False, server_default="未命名配置"),
    )


def downgrade() -> None:
    op.drop_column("policy_revisions", "name")
