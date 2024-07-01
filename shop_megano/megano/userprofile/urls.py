from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import (
    UserLogin,
    UserRegister,
    UserProfileDetails,
    UserAvatarUpdate,
    UserPasswordChange,
)

# app_name = 'userprofile'

urlpatterns = [
    path("api/sign-in", UserLogin, name="login"),
    path("api/sign-up", UserRegister, name="register"),
    path("api/sign-out", LogoutView.as_view(), name="logout"),
    path("api/profile", UserProfileDetails.as_view(), name="user-profile-details"),
    path("api/profile/password", UserPasswordChange.as_view(), name="password-change"),
    path("api/profile/avatar", UserAvatarUpdate.as_view(), name="avatar-update"),
]
