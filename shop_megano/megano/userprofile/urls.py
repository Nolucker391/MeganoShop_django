from django.urls import path
from .views import (
    sign_in,
)

urlpatterns = [
    path('api/sign-in/', sign_in, name='login'),
]



