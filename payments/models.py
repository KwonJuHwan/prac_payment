from django.db import models
from accounts.models import User

class Account(models.Model):
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name="accounts"
    )
    number = models.CharField(max_length=20, unique=True, verbose_name="계좌번호")
    TYPE_CHECKING = 'checking'
    TYPE_SAVING = 'saving'
    TYPE_LOAN = 'loan'
    ACCOUNT_TYPE_CHOICES = [
        (TYPE_CHECKING, '입출금'),
        (TYPE_SAVING, '정기예금'),
        (TYPE_LOAN, '대출'),
    ]
    account_type = models.CharField(max_length=10, choices=ACCOUNT_TYPE_CHOICES, verbose_name="계좌 유형")
    balance = models.DecimalField(max_digits=18, decimal_places=2, default=0, verbose_name="계좌 잔액")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.number} ({self.get_account_type_display()})"

class AccountLog(models.Model):
    account = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        related_name='logs'
    )
    TYPE_DEPOSIT = 'deposit'
    TYPE_WITHDRAW = 'withdraw'
    TRANSACTION_TYPE_CHOICES = [
        (TYPE_DEPOSIT, '입금'),
        (TYPE_WITHDRAW, '출금'),
    ]
    transaction_type = models.CharField(
    max_length=10,
        choices=TRANSACTION_TYPE_CHOICES
    )
    amount = models.DecimalField(max_digits=18, decimal_places=2, verbose_name="거래 금액") 
    balance_after = models.DecimalField(max_digits=18, decimal_places=2, verbose_name="거래 후 잔액")  
    description = models.CharField(max_length=100, blank=True, verbose_name="비고")  
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"[{self.get_transaction_type_display()}] {self.amount}원"

