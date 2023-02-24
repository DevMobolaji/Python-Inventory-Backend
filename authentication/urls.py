from django.urls import path
from .views import RegisterView, verifyEmail, LoginAPIView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginAPIView.as_view(), name="login"),
    path("email-verify/", verifyEmail.as_view(), name="email-verification")
]
