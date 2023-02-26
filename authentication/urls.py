from django.urls import path
from .views import RegisterView, verifyEmail, LoginAPIView, PasswordTokenCheckAPI, RequestPasswordEmail, SetNewPasswordAPIView
from rest_framework_simplejwt.views import (
    TokenRefreshView
)
urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginAPIView.as_view(), name="login"),
    path("email-verify/", verifyEmail.as_view(), name="email-verification"),
    path("request-reset-email/", RequestPasswordEmail.as_view(), name="reset-email"),
    path("password-reset/<uidb64>/<token>/",
         PasswordTokenCheckAPI.as_view(), name="password-reset-confirm"),
    path("password-reset-complete/",
         SetNewPasswordAPIView.as_view(), name="password-reset-complete"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="refresh")
]
