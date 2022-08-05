from .models import User
from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from phonenumber_field.serializerfields import PhoneNumberField

class UserCreationSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=25)
    email = serializers.EmailField(max_length=80)
    phone_number = PhoneNumberField(allow_null=False,allow_blank=False)
    address = serializers.CharField(allow_null=True)
    password = serializers.CharField(min_length=8, write_only=True)

    class Meta:
        model = User    
        fields = ['username','email','phone_number','address','password']

    def validate(self,attrs):
        username_exist = User.objects.filter(username = attrs['username']).exists()

        if username_exist:
            raise serializers.ValidationError(detail = "User with username exists")

        email_exist = User.objects.filter(email = attrs['email']).exists()

        if email_exist:
            raise serializers.ValidationError(detail = "User with this email exists")

        phone_number_exist = User.objects.filter(phone_number = attrs['phone_number']).exists()

        if phone_number_exist:
            raise serializers.ValidationError(detail = "User with this phone_number exists")

        return super().validate(attrs)

    def create(self,validated_data):
        new_user=User(**validated_data)

        new_user.password=make_password(validated_data.get('password'))

        new_user.save()

        return new_user