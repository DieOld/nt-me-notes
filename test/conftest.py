import pytest
import asyncio


@pytest.fixture
def loop():
    return asyncio.get_event_loop()
