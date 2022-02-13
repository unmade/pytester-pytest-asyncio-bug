from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from pytest import FixtureRequest

pytest_plugins = ["pytester"]


@pytest.fixture(scope="session")
def event_loop():
    """Redefine pytest-asyncio event_loop fixture with 'session' scope."""
    loop = asyncio.get_event_loop_policy().get_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def setup() -> None:
    ...


@pytest.fixture(autouse=True)
async def teardown(request: FixtureRequest):
    try:
        yield
    finally:
        pass
