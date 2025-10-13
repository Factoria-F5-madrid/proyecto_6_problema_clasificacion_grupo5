"""add passenger features columns

Revision ID: <REPLACE_WITH_REVISION_ID>
Revises: 
Create Date: 2025-10-11 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '<REPLACE_WITH_REVISION_ID>'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Add new columns to airline_passenger_satisfaction
    op.add_column('airline_passenger_satisfaction',
        sa.Column('type_of_travel', sa.String(), nullable=True)
    )
    op.add_column('airline_passenger_satisfaction',
        sa.Column('inflight_wifi_service', sa.Float(), nullable=True)
    )
    op.add_column('airline_passenger_satisfaction',
        sa.Column('departure_arrival_time_convenient', sa.Float(), nullable=True)
    )
    op.add_column('airline_passenger_satisfaction',
        sa.Column('ease_of_online_booking', sa.Float(), nullable=True)
    )
    op.add_column('airline_passenger_satisfaction',
        sa.Column('gate_location', sa.Float(), nullable=True)
    )
    op.add_column('airline_passenger_satisfaction',
        sa.Column('online_boarding', sa.Float(), nullable=True)
    )
    op.add_column('airline_passenger_satisfaction',
        sa.Column('on_board_service', sa.Float(), nullable=True)
    )
    op.add_column('airline_passenger_satisfaction',
        sa.Column('leg_room_service', sa.Float(), nullable=True)
    )
    op.add_column('airline_passenger_satisfaction',
        sa.Column('inflight_service', sa.Float(), nullable=True)
    )


def downgrade():
    # Drop the columns in reverse order
    op.drop_column('airline_passenger_satisfaction', 'inflight_service')
    op.drop_column('airline_passenger_satisfaction', 'leg_room_service')
    op.drop_column('airline_passenger_satisfaction', 'on_board_service')
    op.drop_column('airline_passenger_satisfaction', 'online_boarding')
    op.drop_column('airline_passenger_satisfaction', 'gate_location')
    op.drop_column('airline_passenger_satisfaction', 'ease_of_online_booking')
    op.drop_column('airline_passenger_satisfaction', 'departure_arrival_time_convenient')
    op.drop_column('airline_passenger_satisfaction', 'inflight_wifi_service')
    op.drop_column('airline_passenger_satisfaction', 'type_of_travel')
