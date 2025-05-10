# services.py

from payments.models import AccountLog
from payments.models import Account

from django.db import transaction
import redis

def process_account_transaction(account, transaction_type, amount):

    if transaction_type == AccountLog.TYPE_DEPOSIT:
        account.balance += amount
    elif transaction_type == AccountLog.TYPE_WITHDRAW:
        if account.balance < amount:
            raise ValueError('잔액이 부족합니다.')
        account.balance -= amount
    else:
        raise ValueError('유효하지 않은 거래 유형입니다.')

    account.save()
    return account.balance

# 비관적락 전체적인 플로우에 모두 적용

def process_account_transaction_pessimistic(account_id, transaction_type, amount):

    with transaction.atomic():
        account = Account.objects.select_for_update().get(id=account_id)
        if transaction_type == AccountLog.TYPE_DEPOSIT:
            account.balance += amount
        elif transaction_type == AccountLog.TYPE_WITHDRAW:
            if account.balance < amount:
                raise ValueError('잔액이 부족합니다.')
            account.balance -= amount
        else:
            raise ValueError('유효하지 않은 거래 유형입니다.')
        account.save()
        return account.balance


# 낙관적 락 (version으로 관리) 업데이트 시점에만 관리
def process_account_transaction_optimistic(account_id, transaction_type, amount):
    with transaction.atomic():
        account = Account.objects.get(id=account_id)
        current_version = account.version

        if transaction_type == AccountLog.TYPE_DEPOSIT:
            account.balance += amount
        elif transaction_type == AccountLog.TYPE_WITHDRAW:
            if account.balance < amount:
                raise ValueError('잔액이 부족합니다.')
            account.balance -= amount
        else:
            raise ValueError('유효하지 않은 거래 유형입니다.')

        updated_rows = Account.objects.filter(
            id=account_id,
            version=current_version
        ).update(
            balance=account.balance,
            version=current_version + 1
        )

        if updated_rows == 0:
            raise Exception("동시성 충돌로 인해 업데이트 실패")
        return account.balance

# 분산락 
# def process_account_transaction(account_id, transaction_type, amount):
#     with transaction.atomic():
#         account = Account.objects.get(id=account_id)
#         if transaction_type == AccountLog.TYPE_DEPOSIT:
#             account.balance += amount
#         elif transaction_type == AccountLog.TYPE_WITHDRAW:
#             if account.balance < amount:
#                 raise ValueError('잔액이 부족합니다.')
#             account.balance -= amount
#         else:
#             raise ValueError('유효하지 않은 거래 유형입니다.')
#         account.save()
#         return account.balance