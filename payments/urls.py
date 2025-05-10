from django.urls import path

from payments.views.create_account import AccountCreateView
from payments.views.pay_account import PayAccountView
from payments.views.post_account_log import AccountLogListView

app_name = "payments"

urlpatterns = [
    path("pay", PayAccountView.as_view(), name="pay order"),
    path("create", AccountCreateView.as_view(), name="creat accounts"),
    path('<str:number>/logs', AccountLogListView.as_view(), name='view account logs'),
]