from django.contrib.auth import authenticate
from django.contrib.auth.models import User

from rest_framework import serializers
from rest_framework.response import Response

from .models import UserProfile


class LoginSerializer(serializers.Serializer):
    """
    Класс - Сериализатор для аунтефикаии пользователя
    """

    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        """
        Валидатор данных
        :param data: dict()
        :return: user
        """
        username = data.get("username")
        password = data.get("password")

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise serializers.ValidationError("Неправильный логин или пароль.")

        data["user"] = user

        return data


class RegisterSerializer(serializers.Serializer):
    """
    Класс сериализатор для регистрации пользователя на сайте.

    """

    username = serializers.CharField(max_length=150)
    name = serializers.CharField(max_length=255, allow_blank=True)
    password = serializers.CharField(write_only=True)

    def validate_username(self, value):
        """
        Валидатор имени пользователя
        :param value:
        :return:
        """
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Имя пользователя занято.")
        return value

    def create(self, validated_data):
        """
        Функция для создания пользователя с указанными параметрами, а так же его профиль.
        :param validated_data:
        :return:
        """
        username = validated_data.get("username")
        password = validated_data.get("password")
        name = validated_data.get("name")

        user = User.objects.create_user(username=username, password=password)
        UserProfile.objects.create(user=user, fullName=name)

        user_auth = authenticate(username=username, password=password)

        return user_auth


class ProfileSerializer(serializers.Serializer):
    """
    Класс сериализатор для обновления информации пользователя на сайте

    """

    fullName = serializers.CharField()
    email = serializers.EmailField()
    phone = serializers.CharField()

    def update(self, instance, validated_data):
        """
        Функция для обновления данных
        :param instance:
        :param validated_data:
        :return:
        """

        instance.userprofile.fullName = validated_data.get("fullName")
        instance.email = validated_data.get("email")
        instance.userprofile.phone = validated_data.get("phone")

        instance.userprofile.email = instance.email

        instance.userprofile.save()
        instance.save()

        return instance


class AvatarSerializer(serializers.Serializer):
    """
    Класс сериализатор для изменения аватарки профиля пользователя.
    """

    avatar = serializers.ImageField()

    def update(self, instance, validated_data):
        """
        Функция для обновления аватарки у пользователя.
        :param instance:
        :param validated_data:
        :return:
        """
        image_file = validated_data.get("avatar")

        if str(image_file).endswith((".png", ".jpg", ".jpeg")):
            instance.userprofile.avatar = image_file
            instance.userprofile.save()

            return instance

        else:
            return Response("Неправильный формат файла.", status=500)


class PasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
