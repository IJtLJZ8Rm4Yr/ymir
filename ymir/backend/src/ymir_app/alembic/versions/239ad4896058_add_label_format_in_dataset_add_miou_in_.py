"""add label_format in dataset, add miou in model

Revision ID: 239ad4896058
Revises: c91513775753
Create Date: 2022-10-26 11:35:59.598597

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "239ad4896058"
down_revision = "c91513775753"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("dataset", schema=None) as batch_op:
        batch_op.add_column(sa.Column("label_format", sa.SmallInteger(), nullable=True))
        batch_op.create_index(batch_op.f("ix_dataset_label_format"), ["label_format"], unique=False)

    with op.batch_alter_table("model", schema=None) as batch_op:
        batch_op.add_column(sa.Column("miou", sa.Float(), nullable=True))

    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("model", schema=None) as batch_op:
        batch_op.drop_column("miou")

    with op.batch_alter_table("dataset", schema=None) as batch_op:
        batch_op.drop_index(batch_op.f("ix_dataset_label_format"))
        batch_op.drop_column("label_format")

    # ### end Alembic commands ###