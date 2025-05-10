from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from payments.serializers import AccountLogCreateSerializer

class PayAccountView(APIView):
    def post(self, request):
        serializer = AccountLogCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)