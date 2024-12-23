import os

import pytest

from app.configs.storage import file_path, store


@pytest.fixture(autouse=True)
def setup_and_teardown():
    store.clear()
    if os.path.exists(file_path):
        os.remove(file_path)
    yield
    store.clear()
    if os.path.exists(file_path):
        os.remove(file_path)
