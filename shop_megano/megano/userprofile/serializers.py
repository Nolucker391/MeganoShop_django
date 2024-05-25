from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.response import Response
from django.contrib.auth.models import User
# from .models import UserProfile

from django.contrib.auth.models import User
from .models import UserProfile

from django.core.exceptions import ValidationError


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):

        username = data.get('username')
        password = data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise serializers.ValidationError('Неправильный логин или пароль.')

        data['user'] = user
        return data


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    name = serializers.CharField(max_length=255, allow_blank=True)
    password = serializers.CharField(write_only=True)

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username is already taken")
        return value

    def create(self, validated_data):
        username = validated_data.get('username')
        password = validated_data.get('password')
        name = validated_data.get('name')

        user = User.objects.create_user(username=username, password=password)
        UserProfile.objects.create(user=user, fullName=name)

        user_auth = authenticate(username=username, password=password)

        return user_auth

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = (
            'id',
            'user',
            'fullName',
            'email',
            'avatar',
            'phone',
        )

    avatar = serializers.SerializerMethodField()

    def get_avatar(self, instance):
        return {'src': f'/media/{instance.avatar.name}',
                'alt': f'{instance.fullName}'}

class UserAvatarSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = 'avatar',
