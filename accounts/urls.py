from django.urls import path

from accounts.views.login import LoginView
from accounts.views.signup import SignUpView

app_name = "accounts"

urlpatterns = [
    path("login", LoginView.as_view(), name="login user"),
    path("signUp", SignUpView.as_view(), name="sign_up user")
]