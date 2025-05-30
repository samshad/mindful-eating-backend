# -----------------------------------------------------------------------------
# Project: Mindful Eating
# Author: Md Samshad Rahman
# Year: 2025
# License: GNU Affero General Public License v3.0 (See LICENSE file for details)
# Description: This file is part of the Mindful Eating project.
# -----------------------------------------------------------------------------
"""Create tables for user, questions, food update and utp

Revision ID: 29605435e345
Revises:
Create Date: 2025-03-04 20:56:39.897569

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "29605435e345"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "otp",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("otp_code", sa.String(), nullable=False),
        sa.Column("expires_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_otp_id"), "otp", ["id"], unique=False)
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("first_name", sa.String(), nullable=False),
        sa.Column("last_name", sa.String(), nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("hashed_password", sa.String(), nullable=False),
        sa.Column("profile_picture", sa.String(), nullable=True),
        sa.Column("dob", sa.Date(), nullable=True),
        sa.Column("age", sa.Integer(), nullable=True),
        sa.Column("username", sa.String(), nullable=True),
        sa.Column("gender_of_birth", sa.String(), nullable=True),
        sa.Column("current_gender", sa.String(), nullable=True),
        sa.Column("occupation", sa.String(), nullable=True),
        sa.Column("lifestyle_type", sa.String(), nullable=True),
        sa.Column("country", sa.String(), nullable=True),
        sa.Column("state", sa.String(), nullable=True),
        sa.Column("city", sa.String(), nullable=True),
        sa.Column("cultural_religious_dietary_influence", sa.String(), nullable=True),
        sa.Column("profile_submission", sa.Boolean(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_users_email"), "users", ["email"], unique=True)
    op.create_index(op.f("ix_users_id"), "users", ["id"], unique=False)
    op.create_table(
        "food_updates",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_food_updates_id"), "food_updates", ["id"], unique=False)
    op.create_table(
        "question_answers",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("question_data", sa.JSON(), nullable=False),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("user_id"),
    )
    op.create_index(
        op.f("ix_question_answers_id"), "question_answers", ["id"], unique=False
    )
    op.create_table(
        "food_images",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("food_update_id", sa.Integer(), nullable=False),
        sa.Column("image_path", sa.String(), nullable=False),
        sa.ForeignKeyConstraint(
            ["food_update_id"],
            ["food_updates.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_food_images_id"), "food_images", ["id"], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_food_images_id"), table_name="food_images")
    op.drop_table("food_images")
    op.drop_index(op.f("ix_question_answers_id"), table_name="question_answers")
    op.drop_table("question_answers")
    op.drop_index(op.f("ix_food_updates_id"), table_name="food_updates")
    op.drop_table("food_updates")
    op.drop_index(op.f("ix_users_id"), table_name="users")
    op.drop_index(op.f("ix_users_email"), table_name="users")
    op.drop_table("users")
    op.drop_index(op.f("ix_otp_id"), table_name="otp")
    op.drop_table("otp")
    # ### end Alembic commands ###
