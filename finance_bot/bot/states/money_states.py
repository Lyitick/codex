"""FSM states for money operations."""
from aiogram.fsm.state import State, StatesGroup


class MoneyStates(StatesGroup):
    """States for handling money operations."""

    choosing_type = State()
    choosing_category = State()
    entering_amount = State()
    entering_comment = State()
    confirming = State()
