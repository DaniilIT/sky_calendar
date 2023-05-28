from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from rest_framework import exceptions, serializers

from core.models import User


class PasswordField(serializers.CharField):
    def __init__(self, **kwargs):
        kwargs['style'] = {'input_type': 'password'}  # для формы drf
        kwargs.setdefault('write_only', True)  # в ответе не указывать
        super().__init__(**kwargs)
        self.validators.append(validate_password)  # проверка на сложность


class UserCreateSerializer(serializers.ModelSerializer):
    password = PasswordField(required=True)
    password_repeat = PasswordField(required=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name',
                  'email', 'password', 'password_repeat')

    def validate(self, attrs: dict):
        if attrs['password'] != attrs['password_repeat']:
            raise exceptions.ValidationError('Passwords do not match')
        del attrs['password_repeat']
        return attrs

    def create(self, validated_data: dict):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)


class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    password = PasswordField(required=True)

    class Meta:
        model = User
        fields = ('username', 'password')

    def create(self, validated_data: dict):
        user = authenticate(
            username=validated_data['username'],
            password=validated_data['password']
        )
        if not user:
            raise exceptions.AuthenticationFailed
        return user
