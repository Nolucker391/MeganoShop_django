import json

from django.contrib.auth import login

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import UpdateModelMixin
from rest_framework import status

from .serializers import (
    LoginSerializer,
    RegisterSerializer,
    AvatarUpdateSerializer,
    ProfileUpdateSerializer,
    PasswordChangeSerializer,
    AvatarSerializer
)

from .models import UserProfile

@api_view(["POST"])
def UserLogin(request: Request):
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
def UserRegister(request: Request):
    """
        Функция описывающая регистрацию пользователя на сайте
    """

    user_data = json.loads(request.body)
    serializer = RegisterSerializer(data=user_data)

    if serializer.is_valid():
        user = serializer.save()
        login(request, user)

        return Response(
            'Успешно зарегистрирован!',
            status=200,
        )
    else:
        return Response(serializer.errors, status=400)


class UserProfileDetails(APIView):
    """
    Класс для отображения профиля пользователя, а так же его заполнение
    """

    def post(self, request):
        """
        Функция обработчик для POST-запроса.
        Обновление данных пользователя
        :param request:
        :return:
        """
        user = request.user

        data = {
            'fullName': request.data.get('fullName'),
            'email': request.data.get('email'),
            'phone': request.data.get('phone'),
        }

        serializer = ProfileUpdateSerializer(data=data)

        if serializer.is_valid():
            serializer.update(user, data)
            return Response(serializer.data, status=200)
        else:
            return Response(serializer.errors, status=400)

    def get(self, request: Request):
        """
        Функция обработчик для GET-запросов
        Демонстрация данных пользователя
        :param request:
        :return:
        """
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

    def post(self, request: Request, ) -> Response:
        user = request.user.pk
        profile = UserProfile.objects.get(user_id=user)

        serializer = AvatarSerializer(instance=profile, data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(
                'Успешно обновлено!',
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# def post(self, request: Request):
    #     user = request.user.pk
    #     userprofile = UserProfile.objects.get(user_id=user)
    #
    #     serializer = AvatarUpdateSerializer(data=request.data, instance=userprofile)
    #
    #     if serializer.is_valid():
    #         userprofile.avatar = serializer.validated_data.get('avatar')
    #         userprofile.save()
    #         #serializer.update(userprofile, serializer.validated_data)
    #         return Response(
    #                 'Update successful',
    #                 status=status.HTTP_200_OK,
    #         )
    #
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # user = request.user
        #
        # data = {
        #     'src': request.data.get('src'),
        #     'alt': request.data.get('alt')
        # }
        #
        # serializer = AvatarUpdateSerializer(instance=user, data=data)
        #
        # if serializer.is_valid():
        #     serializer.update(user, data)
        #     return Response(serializer.data, status=200)
        # else:
        #     return Response(serializer.errors, status=400)




class UserPasswordChange(GenericAPIView, UpdateModelMixin):
    serializer_class = PasswordChangeSerializer

    def get_object(self):
        if self.request.user.is_authenticated:
            return self.request.user

    def post(self, *args, **kwargs):
        return self.update(self.request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        self.object_user = self.get_object()

        data = {
            'current_password': request.data.get('currentPassword'),
            'new_password': request.data.get('newPassword')
        }

        serializer = self.get_serializer(data=data)

        if serializer.is_valid():
            if not self.object_user.check_password(serializer.data.get("current_password")):
                return Response(
                    {'Error': 'Wrong Current Password'},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            self.object_user.set_password(serializer.data.get('new_password'))
            self.object_user.save()

            login(request, self.object_user)

            return Response(
                'Update successful',
                status=status.HTTP_200_OK,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
