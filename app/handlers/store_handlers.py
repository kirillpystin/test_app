import asyncio
import json
import time

from app.configs.storage import file_path, store, store_lock


async def cleanup_expired_items() -> None:
    """Очистка хранилища по TTL"""
    while True:
        now: float = time.time()
        with store_lock:
            keys_to_delete: list[str] = [
                key
                for key, item in store.items()
                if item["expiration"] and item["expiration"] < now
            ]
            for key in keys_to_delete:
                del store[key]
        save_store_to_file()
        await asyncio.sleep(10)


def load_store_from_file() -> None:
    """Загрузка из файла"""
    try:
        with open(file_path, "r") as f:
            data: dict = json.load(f)
            now: float = time.time()
            with store_lock:
                for key, item in data.items():
                    if not item["expiration"] or item["expiration"] > now:
                        store[key] = item
    except FileNotFoundError:
        pass


def save_store_to_file() -> None:
    """Сохранение в файл"""
    with store_lock:
        with open(file_path, "w") as f:
            json.dump(store, f)
