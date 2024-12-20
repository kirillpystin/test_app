"""Конфигурация для хранилища"""
from threading import Lock

store = {}
store_lock = Lock()
file_path = "store.json"
