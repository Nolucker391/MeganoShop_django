import json

from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from rest_framework.decorators import api_view
from django.http import HttpRequest, HttpResponse
from rest_framework.response import Response
from django.urls import reverse_lazy
from rest_framework.views import APIView
from rest_framework.generics import UpdateAPIView
from django.contrib.auth.hashers import check_password, make_password
from rest_framework.parsers import JSONParser
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import UpdateModelMixin

from .serializers import (
    LoginSerializer,
    RegisterSerializer,
    AvatarUpdateSerializer,
    ProfileUpdateSerializer,
    PasswordChangeSerializer,
)
from rest_framework import status

from django.contrib.auth.models import User
from .models import UserProfile

class UserProfileDetails(APIView):
    def post(self, request):
        user = request.user

        data = {
            'fullName': request.data.get('fullName'),
            'email': request.data.get('email'),
            'phone': request.data.get('phone')
        }

        serializer = ProfileUpdateSerializer(data=data)

        if serializer.is_valid():
            serializer.update(user, data)
            return Response(serializer.data, status=200)
        else:
            return Response(serializer.errors, status=400)

    def get(self, request: HttpRequest):
        if request.user.is_authenticated:
            user = request.user

            data = {
                'fullName': user.userprofile.fullName,
                'email': user.email,
                'phone': user.userprofile.phone,
            }
            if user.userprofile.avatar:
                data['avatar'] = {
                    'src': user.userprofile.avatar.url,
                    'alt': user.userprofile.avatar.name,
                }
            return Response(data=data, status=200)
        return Response(status=400)


class UserAvatarUpdate(APIView):

    def post(self, request: HttpRequest):
        user = request.user

        data = {
            'src': request.data.get('src'),
            'alt': request.data.get('alt')
        }

        serializer = AvatarUpdateSerializer(instance=user, data=data)

        if serializer.is_valid():
            serializer.update(user, data)
            return Response(serializer.data, status=200)
        else:
            return Response(serializer.errors, status=400)

        # user = request.user.pk
        # userprofile = UserProfile.objects.get(user_id=user)
        #
        # serializer = AvatarUpdateSerializer(data=request.data, instance=userprofile)
        #
        # if serializer.is_valid():
        #     userprofile.avatar = serializer.validated_data.get('avatar')
        #     userprofile.save()
        #     #serializer.update(userprofile, serializer.validated_data)
        #     return Response(
        #             'Update successful',
        #             status=status.HTTP_200_OK,
        #     )
        #
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        #
class UserPasswordChange(GenericAPIView, UpdateModelMixin):
    serializer_class = PasswordChangeSerializer

    def get_object(self):
        return self.request.user

    def post(self, *args, **kwargs):
        return self.update(self.request, *args, **kwargs)
    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        data = {
            'passwordCurrent': request.data.get('passwordCurrent'),
            'passwordReply': request.data.get('passwordReply'),
            'password': request.data.get('password')
        }
        print(request.data)
        serializer = self.get_serializer(data=data)
        print(serializer.is_valid)
        if serializer.is_valid():
            if not self.object.check_password(
                    serializer.data.get("currentPassword")
            ):
                return Response(
                    {'Error': 'Wrong Current Password'},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            self.object.set_password(serializer.data.get('newPassword'))
            self.object.save()
            return Response(
                'Update successful',
                status=status.HTTP_200_OK,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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






