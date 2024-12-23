"""Конфигурация для prometheus"""

from prometheus_client import Counter, Gauge

items_stored = Counter("items_stored", "Total number of items stored")
active_items = Gauge("active_items", "Current number of active items in store")
