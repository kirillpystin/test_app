"""Конфигурация для хранилища"""
import asyncio

store = {}
store_lock = asyncio.Lock()
file_path = "store.json"
