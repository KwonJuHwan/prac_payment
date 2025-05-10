from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from accounts.serializers import SignUpSerializer
from django.contrib.auth import authenticate
from rest_framework import status

class SignUpView(APIView):
    permission_classes = [AllowAny]
    serializer_class = SignUpSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            {"message": "회원가입이 완료되었습니다."},
            status=status.HTTP_201_CREATED
        )
        
