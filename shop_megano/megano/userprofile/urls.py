from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import (
    sign_in,
    UserRegister,
    UserProfileDetails,
    UserAvatarUpdate,
)

urlpatterns = [
    path('api/sign-in/', sign_in, name='login'),
    path('api/sign-out/', LogoutView.as_view(), name='logout'),
    path('api/sign-up/', UserRegister, name='register'),

    path('api/profile/', UserProfileDetails.as_view(), name='user-profile-details'),
    path('api/profile/avatar', UserAvatarUpdate.as_view(), name='avatar_update'),
]



