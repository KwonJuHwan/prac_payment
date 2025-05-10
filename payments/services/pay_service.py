# services.py

from payments.models import AccountLog

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
