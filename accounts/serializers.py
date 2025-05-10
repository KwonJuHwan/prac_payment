from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from .models import User

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = 'email' 

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['grade'] = user.grade
        return token
    

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, error_messages={'required': '이메일을 입력해 주세요.'})
    password = serializers.CharField(required=True, write_only=True, error_messages={'required': '비밀번호를 입력해 주세요.'})
    
class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password', 'name')
        extra_kwargs = {'password': {'write_only': True}}
    
    def create(self, validated_data):
        user = User.objects.create_user(
            email = validated_data['email'],
            password = validated_data['password'],
            name = validated_data['name']
        )
        return user
    