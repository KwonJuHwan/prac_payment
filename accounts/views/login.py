from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from accounts.serializers import CustomTokenObtainPairSerializer, LoginSerializer
from django.contrib.auth import authenticate
from rest_framework import status

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        email = data['email']
        password = data['password']

        user = authenticate(request, username=email, password=password)
        if not user:
            return Response(
                {'errors': '이메일 또는 비밀번호가 올바르지 않습니다.'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        serializer = CustomTokenObtainPairSerializer(data={
            'email': email,
            'password': password
        })
        serializer.is_valid(raise_exception=True) 
        return Response(serializer.validated_data, status=status.HTTP_200_OK)