import json

from django.contrib.auth import login, authenticate
from django.shortcuts import render
from rest_framework.decorators import api_view
from django.http import HttpRequest
from rest_framework.response import Response

from .serializers import LoginSerializer
from rest_framework import status


@api_view(["POST"])
def sign_in(request: HttpRequest):
    user_data = json.loads(list(request.data.dict().keys())[0])

    user = authenticate(
        username=user_data.get('username'),
        password=user_data.get('password'),
    )

    if user:
        login(request, user)
        return Response(status=200)
    return Response(status=500)
    #serializer = LoginSerializer(data=user_data)

    # if serializer.is_valid(raise_exception=True):
    #     user = serializer.validated_data['user']
    #     login(request, user)
    #
    #     return Response('Вы успешно авторизовались!', status=200)
    # else:
    #     return Response(serializer.errors, status=401)