import os

import pytest
from fastapi.testclient import TestClient

from app import app
from app.configs.storage import file_path, store

client = TestClient(app)


@pytest.fixture(scope="function")
def setup_and_teardown():
    store.clear()
    if os.path.exists(file_path):
        os.remove(file_path)
    yield
    store.clear()
    if os.path.exists(file_path):
        os.remove(file_path)
