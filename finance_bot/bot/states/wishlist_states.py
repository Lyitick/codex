"""FSM states for wishlist operations."""
from aiogram.fsm.state import State, StatesGroup


class WishlistStates(StatesGroup):
    """States for handling wishlist items."""

    entering_title = State()
    entering_amount = State()
    entering_priority = State()
    confirming = State()
