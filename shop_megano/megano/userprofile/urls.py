from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import (
    sign_in,
    UserRegister,
    UserProfileDetails,
    UserAvatarUpdate,
    UserPasswordChange
)

urlpatterns = [
    path('api/profile', UserProfileDetails.as_view(), name='user-profile-details'),
    path('api/profile/password', UserPasswordChange.as_view(), name='password-change'),
    path('api/profile/avatar', UserAvatarUpdate.as_view(), name='avatar-update'),
    path('api/sign-in', sign_in, name='login'),
    path('api/sign-out', LogoutView.as_view(), name='logout'),
    path('api/sign-up', UserRegister, name='register'),
]



