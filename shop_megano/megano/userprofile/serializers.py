from django.contrib.auth import authenticate, password_validation
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

class ProfileUpdateSerializer(serializers.Serializer):
    fullName = serializers.CharField()
    email = serializers.EmailField()
    phone = serializers.CharField()

    def update(self, instance, validated_data):
        instance.userprofile.fullName = validated_data.get('fullName')
        instance.email = validated_data.get('email')
        instance.userprofile.phone = validated_data.get('phone')
        instance.userprofile.save()
        instance.save()
        return instance


class AvatarUpdateSerializer(serializers.Serializer):
    avatar = serializers.ImageField()

    def update(self, instance, validated_data):
        image_file = validated_data.get('avatar')
        if str(image_file).endswith(('.png', '.jpg', '.jpeg')):
            instance.userprofile.avatar = image_file
            if instance.userprofile.avatar.size < 2 * 1024 * 1024:
                instance.userprofile.save()
                instance.save()
            else:
                return Response(
                    {
                        "error": "Invalid file format",
                        "details": "The uploaded file is not a supported image",
                    },
                    status=400
                )
        else:
            return Response(
                    {
                        "error": "Invalid file format",
                        "details": "'Wrong file format'",
                    },
                    status=400
                )

        return instance

        # image_file = validated_data.FILES["avatar"]
        # if str(image_file).endswith(('.png', '.jpg', '.jpeg')):
        #     instance.userprofile.avatar = image_file
        #     if instance.userprofile.avatar and instance.userprofile.avatar.size < 2 * 1024 * 1024:
        #         instance.userprofile.save()
        #         instance.save()
        #     else:
        #         return Response('avatar bigger then 2 mb or no avatar provided', status=400)
        # else:
        #     return Response('Wrong file format', status=400)
        #
        # return instance

class PasswordChangeSerializer(serializers.Serializer):
    passwordCurrent = serializers.CharField(required=True)
    passwordReply = serializers.CharField(required=True)
    password = serializers.CharField(required=True)




