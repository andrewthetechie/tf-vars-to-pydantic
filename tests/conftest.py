from pathlib import Path

import pytest


@pytest.fixture
def fixture_path() -> Path:
    yield Path("./tests/fixtures")
