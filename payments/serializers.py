from rest_framework import serializers
from .models import AccountLog, Account
from .services.pay_service import process_account_transaction

class AccountCreateSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.name', read_only=True)

    class Meta:
        model = Account
        fields = [
            'user_name',    
            'number',      
            'account_type', 
            'created_at',   
        ]
        read_only_fields = ['user_name', 'created_at']

    def validate_account_type(self, value):
        valid_types = [choice[0] for choice in Account.ACCOUNT_TYPE_CHOICES]
        if value not in valid_types:
            raise serializers.ValidationError(
                f"유효하지 않은 계좌 유형입니다. 허용값: {', '.join(valid_types)}"
            )
        return value

class AccountLogCreateSerializer(serializers.ModelSerializer):
    number = serializers.CharField(write_only=True)
    transaction_type_display = serializers.SerializerMethodField(read_only=True) 

    class Meta:
        model = AccountLog
        fields = [
            'number',       
            'transaction_type', 
            'transaction_type_display',     
            'amount',
            'balance_after',                
            'description',           
            'created_at',           
        ]
        read_only_fields = ['created_at', 'balance_after', 'transaction_type_display']
    
    ## Django 모델에서 choices 옵션이 적용된 필드는
    ## 자동으로 get_필드명_display() 메서드가 생성

    def get_transaction_type_display(self, obj):
        return obj.get_transaction_type_display()
    
    def validate(self, attrs):
        try:
            account = Account.objects.get(number=attrs['number'])
        except Account.DoesNotExist:
            raise serializers.ValidationError({'account_number': '존재하지 않는 계좌번호입니다.'})
        
        transaction_type = attrs.get('transaction_type')
        valid_types = [choice[0] for choice in AccountLog.TRANSACTION_TYPE_CHOICES]
        if transaction_type not in valid_types:
            raise serializers.ValidationError({
                'transaction_type': f"유효하지 않은 거래 유형입니다. 허용값: {', '.join(valid_types)}"
            })
        
        attrs['account'] = account
        return attrs

    def create(self, validated_data):
        validated_data.pop('number')
        account = validated_data['account']
        transaction_type = validated_data['transaction_type']
        amount = validated_data['amount']

        try:
            new_balance = process_account_transaction(account, transaction_type, amount)
        except ValueError as e:
            raise serializers.ValidationError({'amount': str(e)})

        validated_data['balance_after'] = new_balance

        return super().create(validated_data)