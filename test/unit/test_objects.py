from test.conftest import client

from app import load_store_from_file
from app.configs.storage import store
from app.handlers.store_handlers import save_store_to_file


def test_create_item(setup_and_teardown):
    response = client.put(
        "/objects/test", json={"data": {"test": "test"}, "expires": 10}
    )
    assert response.status_code == 200
    assert response.json() == {"message": "Item stored successfully."}
    assert "test" in store


def test_get_item(setup_and_teardown):
    client.put("/objects/test", json={"data": {"test1": "test1"}, "expires": 100})
    response = client.get("/objects/test")
    assert response.status_code == 200
    assert response.json() == {"test1": "test1"}


def test_liveness():
    response = client.get("/health/liveness")
    assert response.status_code == 200
    assert response.json() == {"status": "alive"}


def test_readiness(setup_and_teardown):
    response = client.get("/health/readiness")
    assert response.status_code == 503

    save_store_to_file()
    response = client.get("/health/readiness")
    assert response.status_code == 200
    assert response.json()["status"] == "ready"


def test_metrics():
    response = client.get("/metrics")
    assert response.status_code == 200
    assert "items_stored" in response.text
    assert "active_items" in response.text


def test_save_and_load_store(setup_and_teardown):
    client.put("/objects/test", json={"data": {"test1": "test1"}})
    save_store_to_file()
    store.clear()
    load_store_from_file()
    assert "test" in store
    assert store["test"]["value"] == {"test1": "test1"}
