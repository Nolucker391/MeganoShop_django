import json

from django.contrib.auth import login, authenticate
from django.shortcuts import render
from rest_framework.decorators import api_view
from django.http import HttpRequest, HttpResponse
from rest_framework.response import Response
from django.urls import reverse_lazy
from rest_framework.views import APIView


from .serializers import LoginSerializer, RegisterSerializer, UserProfileSerializer, UserAvatarSerializer
from rest_framework import status

from django.contrib.auth.models import User
from .models import UserProfile

class UserProfileDetails(APIView):
    def get(self, request: HttpRequest) -> Response:
        user = request.user.pk
        profile = UserProfile.objects.get(user_id=user)
        serializer = UserProfileSerializer(profile, many=False)
        return Response(serializer.data)

    def post(self, request: HttpRequest) -> Response:
        user = request.user.pk
        profile = UserProfile.objects.get(user_id=user)
        profile.fullName = request.data.get('fullName')
        profile.phone = request.data.get('phone')
        profile.email = request.data.get('email')
        profile.save()
        serialized = UserProfileSerializer(profile, many=False)
        return Response(serialized.data)

class UserAvatarUpdate(APIView):
    serializer_class = UserAvatarSerializer
    def post(self, request: HttpRequest) -> Response:
        new_avatar = request.FILES['avatar']
        user = request.user.pk
        profile = UserProfile.objects.get(user_id=user)
        profile.avatar = new_avatar
        profile.save()

        return Response(
            "Успешно обновлено.",
            status=200,
        )

@api_view(["POST"])
def sign_in(request: HttpRequest):
    """
       Функция для входа пользователя в систему
    """

    user_data = json.loads(list(request.data.dict().keys())[0])

    serializer = LoginSerializer(data=user_data)

    if serializer.is_valid(raise_exception=True):
        user = serializer.validated_data['user']
        login(request, user)

        return Response('Вы успешно авторизовались!', status=200)
    else:
        return Response(data=serializer.errors, status=400)



@api_view(["POST"])
def UserRegister(request: HttpRequest):
    """
        Функция описывающая регистрацию пользователя на сайте
    """

    user_data = json.loads(request.body)
    serializer = RegisterSerializer(data=user_data)


    if serializer.is_valid():
        user = serializer.save()

        login(request, user)

        return Response(
            'Successful registration',
            status=200,
        )
    else:
        return Response(serializer.errors, status=400)






