from wsgiref import validate
from rest_framework import serializers
from accounts.models import Administrator, Student, User
from django.core.exceptions import ObjectDoesNotExist
from rest_framework_simplejwt.serializers import TokenObtaibPairSerializer
from rest_framework_simplejwt.settings import api_settings
from django.contrib.auth.models import update_last_login
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import DjangoUnicodeDecodeError, force_str, smart_bytes, smart_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework.exceptions import AuthenticationFailed


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email", "full_name", "phone", "timestamp")
        read_only_fields = ("id", "timestamp")

class LoginSerializer(TokenObtaibPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data["user"] = UserSerializer(self.user).data
        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)
        return data

class StudentRegistrationSerializer(serializers.ModelSerializer):
    