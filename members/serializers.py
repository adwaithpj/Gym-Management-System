from rest_framework import serializers
from .models import Subscription,Paymentmethod,GymMembers
from authentication.models import GymAdmin

class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ['subs']

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paymentmethod
        fields = ['method']

class CreatedBySerializer(serializers.ModelSerializer):
    class Meta:
        model = GymAdmin
        fields = ['username','email']
        
class GymMembersSerializer(serializers.ModelSerializer):
    
    sub_type = serializers.PrimaryKeyRelatedField(queryset=Subscription.objects.all(), write_only=True)
    sub_type_details = SubscriptionSerializer(source = 'sub_type',read_only=True)
    
    pay_method = serializers.PrimaryKeyRelatedField(queryset=Paymentmethod.objects.all(), write_only=True)
    pay_method_details = PaymentSerializer(source = 'pay_method',read_only=True)
    
    created_by = serializers.PrimaryKeyRelatedField(queryset=GymAdmin.objects.all(), write_only=True)
    created_by_details = CreatedBySerializer(source = 'created_by',read_only=True)
    
    # user_profile_image = serializers.ImageField(write_only=True, required=False)
    
    class Meta:
        model = GymMembers
        fields = '__all__'
        # exclude = ['user_profile_image']
    
    def validate_email(self, value):
        lower_email = value.lower()
        if GymMembers.objects.filter(email__iexact=lower_email).exists():
            raise serializers.ValidationError("Duplicate")
        return lower_email
    
    def validate(self, data):
        
        if len(data['phone_number']) > 10:
            raise serializers.ValidationError("Phone Number must be at least 10 characters")
        return data

    # def create(self, validated_data):
    #     user_profile_image = validated_data.pop('user_profile_image', None)
        
    #     instance = super().create(validated_data)
        
    #     if user_profile_image:
    #         instance.user_profile_image = user_profile_image
    #         instance.save()
        
    #     return instance