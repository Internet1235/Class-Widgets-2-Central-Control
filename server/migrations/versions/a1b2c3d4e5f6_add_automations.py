"""add automation rules and runs

Revision ID: a1b2c3d4e5f6
Revises: ddf8a4e91c2b
"""

from collections.abc import Sequence
from uuid import uuid4

import sqlalchemy as sa
from alembic import op

revision: str = "a1b2c3d4e5f6"
down_revision: str | Sequence[str] | None = "ddf8a4e91c2b"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column("devices", sa.Column("online_session_id", sa.String(length=36), nullable=True))
    connection = op.get_bind()
    device_ids = connection.execute(sa.text("SELECT id FROM devices WHERE online_session_id IS NULL")).scalars().all()
    for device_id in device_ids:
        connection.execute(
            sa.text("UPDATE devices SET online_session_id = :session_id WHERE id = :device_id"),
            {"session_id": str(uuid4()), "device_id": device_id},
        )
    with op.batch_alter_table("devices") as batch:
        batch.alter_column("online_session_id", nullable=False)

    op.create_table(
        "automation_rules",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("organization_id", sa.String(length=36), nullable=False),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("enabled", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("trigger_type", sa.String(length=20), nullable=False),
        sa.Column("scheduled_time", sa.String(length=5), nullable=True),
        sa.Column("weekdays", sa.JSON(), nullable=False),
        sa.Column("run_date", sa.Date(), nullable=True),
        sa.Column("condition_operator", sa.String(length=3), nullable=False, server_default="and"),
        sa.Column("conditions", sa.JSON(), nullable=False),
        sa.Column("condition_type", sa.String(length=20), nullable=False, server_default="always"),
        sa.Column("condition_value", sa.String(length=80), nullable=False, server_default=""),
        sa.Column("delay_seconds", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("group_id", sa.String(length=36), nullable=True),
        sa.Column("device_id", sa.String(length=36), nullable=True),
        sa.Column("action_type", sa.String(length=20), nullable=False),
        sa.Column("action_payload", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["organization_id"], ["organizations.id"]),
        sa.ForeignKeyConstraint(["group_id"], ["device_groups.id"]),
        sa.ForeignKeyConstraint(["device_id"], ["devices.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_automation_rules_organization_id", "automation_rules", ["organization_id"])
    op.create_index("ix_automation_rules_enabled", "automation_rules", ["enabled"])
    op.create_table(
        "automation_runs",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("rule_id", sa.String(length=36), nullable=False),
        sa.Column("device_id", sa.String(length=36), nullable=False),
        sa.Column("scheduled_for", sa.DateTime(timezone=True), nullable=False),
        sa.Column("session_key", sa.String(length=120), nullable=False),
        sa.Column("execute_after", sa.DateTime(timezone=True), nullable=False),
        sa.Column("status", sa.String(length=20), nullable=False, server_default="pending"),
        sa.Column("reason", sa.String(length=500), nullable=False, server_default=""),
        sa.Column("command_id", sa.String(length=36), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("finished_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["rule_id"], ["automation_rules.id"]),
        sa.ForeignKeyConstraint(["device_id"], ["devices.id"]),
        sa.ForeignKeyConstraint(["command_id"], ["commands.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("rule_id", "device_id", "session_key"),
    )
    op.create_index("ix_automation_runs_rule_id", "automation_runs", ["rule_id"])
    op.create_index("ix_automation_runs_device_id", "automation_runs", ["device_id"])
    op.create_index("ix_automation_runs_execute_after", "automation_runs", ["execute_after"])
    op.create_index("ix_automation_runs_status", "automation_runs", ["status"])


def downgrade() -> None:
    op.drop_index("ix_automation_runs_status", table_name="automation_runs")
    op.drop_index("ix_automation_runs_execute_after", table_name="automation_runs")
    op.drop_index("ix_automation_runs_device_id", table_name="automation_runs")
    op.drop_index("ix_automation_runs_rule_id", table_name="automation_runs")
    op.drop_table("automation_runs")
    op.drop_index("ix_automation_rules_enabled", table_name="automation_rules")
    op.drop_index("ix_automation_rules_organization_id", table_name="automation_rules")
    op.drop_table("automation_rules")
    with op.batch_alter_table("devices") as batch:
        batch.drop_column("online_session_id")