from rest_framework import generics
from payments.models import Account, AccountLog
from rest_framework.exceptions import PermissionDenied
from payments.serializers import AccountLogCreateSerializer

class AccountLogListView(generics.ListAPIView):
    serializer_class = AccountLogCreateSerializer

    def get_queryset(self):
        account_number = self.kwargs['number']
        user = self.request.user

        try:
            account = Account.objects.get(number=account_number, user=user)
        except Account.DoesNotExist:
            raise PermissionDenied("해당 계좌에 접근할 권한이 없습니다.")

        return AccountLog.objects.filter(account=account).order_by('-created_at')
