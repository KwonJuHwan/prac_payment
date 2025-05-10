import redis

class RedisLockManager:
    def __init__(self, redis_client):
        self.redis_client = redis_client

    def acquire_lock(self, key, timeout=10, wait_timeout=5):
        lock = self.redis_client.lock(key, timeout=timeout)
        acquired = lock.acquire(blocking=True, timeout=wait_timeout)
        return lock if acquired else None

    def release_lock(self, lock):
        if lock:
            try:
                lock.release()
            except Exception:
                pass