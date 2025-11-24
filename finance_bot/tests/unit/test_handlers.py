"""Handler tests with simple mocks."""
import asyncio
from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest

from bot.handlers.start import cmd_start
from bot.handlers.finances import finance_entry
from bot.states.money_states import MoneyStates


@pytest.mark.asyncio
async def test_start_handler_creates_message(monkeypatch) -> None:
    """Start handler should send greeting."""
    message = AsyncMock()
    message.from_user.id = 1
    message.answer = AsyncMock()
    # mock database context manager
    async def empty_session():
        if False:
            yield None

    monkeypatch.setattr("bot.handlers.start.get_session", empty_session)
    await cmd_start(message)
    message.answer.assert_called()


@pytest.mark.asyncio
async def test_finance_entry_sets_state() -> None:
    """Finance entry should set FSM state."""
    message = AsyncMock()
    message.answer = AsyncMock()
    state = AsyncMock()
    state.set_state = AsyncMock()
    await finance_entry(message, state)
    state.set_state.assert_called_with(MoneyStates.choosing_type)
