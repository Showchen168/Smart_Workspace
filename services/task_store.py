"""
任務存儲服務
支援 Redis 和記憶體兩種模式
"""
import json
import os
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any


class TaskStore(ABC):
    """任務存儲抽象基類"""

    @abstractmethod
    def get(self, task_id: str) -> dict | None:
        """取得任務"""
        pass

    @abstractmethod
    def set(self, task_id: str, data: dict) -> None:
        """設定任務"""
        pass

    @abstractmethod
    def update(self, task_id: str, updates: dict) -> None:
        """更新任務部分欄位"""
        pass

    @abstractmethod
    def exists(self, task_id: str) -> bool:
        """檢查任務是否存在"""
        pass

    @abstractmethod
    def get_all(self) -> list[dict]:
        """取得所有任務"""
        pass

    @abstractmethod
    def delete(self, task_id: str) -> None:
        """刪除任務"""
        pass


class MemoryTaskStore(TaskStore):
    """記憶體存儲（開發/測試用）"""

    def __init__(self):
        self._store: dict[str, dict] = {}

    def get(self, task_id: str) -> dict | None:
        return self._store.get(task_id)

    def set(self, task_id: str, data: dict) -> None:
        self._store[task_id] = data

    def update(self, task_id: str, updates: dict) -> None:
        if task_id in self._store:
            self._store[task_id].update(updates)

    def exists(self, task_id: str) -> bool:
        return task_id in self._store

    def get_all(self) -> list[dict]:
        return list(self._store.values())

    def delete(self, task_id: str) -> None:
        if task_id in self._store:
            del self._store[task_id]


class RedisTaskStore(TaskStore):
    """Redis 存儲（生產環境用）"""

    def __init__(self, host: str = 'localhost', port: int = 6379, db: int = 0,
                 prefix: str = 'task:', ttl: int = 86400):
        """
        初始化 Redis 連接

        Args:
            host: Redis 主機
            port: Redis 端口
            db: Redis 資料庫編號
            prefix: Key 前綴
            ttl: 任務過期時間（秒），預設 24 小時
        """
        try:
            import redis
            self._redis = redis.Redis(host=host, port=port, db=db, decode_responses=True)
            self._redis.ping()
        except Exception as e:
            raise ConnectionError(f"無法連接 Redis: {e}")

        self._prefix = prefix
        self._ttl = ttl

    def _key(self, task_id: str) -> str:
        """生成完整的 Redis key"""
        return f"{self._prefix}{task_id}"

    def get(self, task_id: str) -> dict | None:
        data = self._redis.get(self._key(task_id))
        if data:
            return json.loads(data)
        return None

    def set(self, task_id: str, data: dict) -> None:
        self._redis.setex(self._key(task_id), self._ttl, json.dumps(data, ensure_ascii=False))

    def update(self, task_id: str, updates: dict) -> None:
        existing = self.get(task_id)
        if existing:
            existing.update(updates)
            self.set(task_id, existing)

    def exists(self, task_id: str) -> bool:
        return self._redis.exists(self._key(task_id)) > 0

    def get_all(self) -> list[dict]:
        keys = self._redis.keys(f"{self._prefix}*")
        tasks = []
        for key in keys:
            data = self._redis.get(key)
            if data:
                tasks.append(json.loads(data))
        return tasks

    def delete(self, task_id: str) -> None:
        self._redis.delete(self._key(task_id))


def create_task_store() -> TaskStore:
    """
    根據環境變數建立適當的任務存儲

    環境變數:
        REDIS_HOST: Redis 主機（設定此項則使用 Redis）
        REDIS_PORT: Redis 端口（預設 6379）
        REDIS_DB: Redis 資料庫（預設 0）
    """
    redis_host = os.getenv('REDIS_HOST')

    if redis_host:
        try:
            return RedisTaskStore(
                host=redis_host,
                port=int(os.getenv('REDIS_PORT', '6379')),
                db=int(os.getenv('REDIS_DB', '0'))
            )
        except ConnectionError as e:
            print(f"警告: Redis 連接失敗，回退到記憶體存儲: {e}")

    return MemoryTaskStore()
