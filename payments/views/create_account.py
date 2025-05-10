from rest_framework import generics, permissions
from payments.models import Account
from payments.serializers import AccountCreateSerializer

class AccountCreateView(generics.CreateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountCreateSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)