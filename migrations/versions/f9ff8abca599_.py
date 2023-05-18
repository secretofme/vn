"""empty message

Revision ID: f9ff8abca599
Revises: 4721615e4989
Create Date: 2023-05-08 21:44:26.047391

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f9ff8abca599'
down_revision = '4721615e4989'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Property_Tables',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('url', sa.String(length=100), nullable=True),
    sa.Column('Number_of_vulnerabilities', sa.Integer(), nullable=True),
    sa.Column('time', sa.DateTime(), nullable=True),
    sa.Column('status', sa.String(length=30), nullable=True),
    sa.Column('create_user', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('Vuln_Tables',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('url', sa.String(length=100), nullable=True),
    sa.Column('vulntype', sa.String(length=100), nullable=True),
    sa.Column('time', sa.DateTime(), nullable=True),
    sa.Column('param', sa.Text(), nullable=True),
    sa.Column('payload', sa.Text(), nullable=True),
    sa.Column('snapshot', sa.Text(), nullable=True),
    sa.Column('create_user', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('username', sa.String(length=50), nullable=False),
    sa.Column('pw_hash', sa.String(length=128), nullable=False),
    sa.Column('email', sa.String(length=20), nullable=True),
    sa.Column('phone', sa.String(length=11), nullable=True),
    sa.Column('description', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('Domain_Tables',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('create_user', sa.String(length=50), nullable=False),
    sa.Column('domain', sa.String(length=30), nullable=False),
    sa.Column('subdomain', sa.String(length=30), nullable=False),
    sa.ForeignKeyConstraint(['create_user'], ['user.username'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('Fingerprint_Tables',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('url', sa.String(length=100), nullable=False),
    sa.Column('fingerprint', sa.String(length=100), nullable=False),
    sa.Column('title', sa.String(length=100), nullable=True),
    sa.Column('create_user', sa.String(length=50), nullable=False),
    sa.ForeignKeyConstraint(['create_user'], ['user.username'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('Port_Tables',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('create_user', sa.String(length=50), nullable=False),
    sa.Column('target_ip', sa.String(length=15), nullable=False),
    sa.Column('target_port', sa.String(length=10), nullable=False),
    sa.Column('status', sa.String(length=20), nullable=False),
    sa.Column('service', sa.String(length=50), nullable=True),
    sa.Column('version', sa.String(length=50), nullable=True),
    sa.ForeignKeyConstraint(['create_user'], ['user.username'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('Spider_Tables',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('create_user', sa.String(length=50), nullable=False),
    sa.Column('url', sa.String(length=100), nullable=False),
    sa.Column('urllist', sa.String(length=100), nullable=False),
    sa.Column('code', sa.String(length=4), nullable=False),
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['create_user'], ['user.username'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('tasklist',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('pid', sa.String(length=128), nullable=False),
    sa.Column('create_user', sa.String(length=50), nullable=False),
    sa.Column('taskname', sa.String(length=100), nullable=False),
    sa.Column('status', sa.String(length=30), nullable=True),
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['create_user'], ['user.username'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('tasklist')
    op.drop_table('Spider_Tables')
    op.drop_table('Port_Tables')
    op.drop_table('Fingerprint_Tables')
    op.drop_table('Domain_Tables')
    op.drop_table('user')
    op.drop_table('Vuln_Tables')
    op.drop_table('Property_Tables')
    # ### end Alembic commands ###
