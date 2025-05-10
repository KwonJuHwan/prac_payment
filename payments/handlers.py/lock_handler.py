import redis
from config.utils import RedisLockManager
from payments.services.pay_service import process_account_transaction

redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)
lock_manager = RedisLockManager(redis_client)

def safe_process_account_transaction(account_id, transaction_type, amount):
    lock_key = f"account_lock_{account_id}"
    lock = lock_manager.acquire_lock(lock_key, timeout=10, wait_timeout=5)
    if not lock:
        raise Exception("다른 작업이 진행 중입니다. 잠시 후 다시 시도해 주세요.")
    try:
        return process_account_transaction(account_id, transaction_type, amount)
    finally:
        lock_manager.release_lock(lock)