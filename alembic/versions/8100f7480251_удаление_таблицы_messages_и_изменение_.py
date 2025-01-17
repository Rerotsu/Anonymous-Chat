"""удаление таблицы messages и изменение всех других таблиц

Revision ID: 8100f7480251
Revises: 001fbf32c246
Create Date: 2025-01-10 16:51:14.764133

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '8100f7480251'
down_revision: Union[str, None] = '001fbf32c246'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_messages_id', table_name='messages')
    op.drop_table('messages')
    op.drop_index('ix_chat_participants_chat_id', table_name='chat_participants')
    op.drop_table('chat_participants')
    op.add_column('chats', sa.Column('user1_id', sa.Integer(), nullable=True))
    op.add_column('chats', sa.Column('user2_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'chats', 'users', ['user2_id'], ['id'])
    op.create_foreign_key(None, 'chats', 'users', ['user1_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'chats', type_='foreignkey')
    op.drop_constraint(None, 'chats', type_='foreignkey')
    op.drop_column('chats', 'user2_id')
    op.drop_column('chats', 'user1_id')
    op.create_table('chat_participants',
    sa.Column('chat_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['chat_id'], ['chats.id'], name='chat_participants_chat_id_fkey'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='chat_participants_user_id_fkey'),
    sa.PrimaryKeyConstraint('chat_id', 'user_id', name='chat_participants_pkey')
    )
    op.create_index('ix_chat_participants_chat_id', 'chat_participants', ['chat_id'], unique=False)
    op.create_table('messages',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('chat_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('content', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('timestamp', postgresql.TIMESTAMP(), server_default=sa.text('now()'), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['chat_id'], ['chats.id'], name='messages_chat_id_fkey'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='messages_user_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='messages_pkey')
    )
    op.create_index('ix_messages_id', 'messages', ['id'], unique=False)
    # ### end Alembic commands ###
