from rest_framework import generics, status, views
from .serializers import (EmailVerificationSerializer, RegisterSerializer,
                          LoginSerializer, RequestPasswordEmailSerializer, SetNewPasswordSerializer)
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from .utils import Util
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.conf import settings
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import jwt
from .renderers import UserRender
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, smart_bytes, DjangoUnicodeDecodeError  # type: ignore
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

# Create your views here.


class RegisterView(generics.GenericAPIView):

    serializer_class = RegisterSerializer
    renderer_classes = (UserRender, )

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        user_data = serializer.data
        user = User.objects.get(email=user_data['email'])

        token = RefreshToken.for_user(user).access_token
        current_site = get_current_site(request).domain

        relative_link = reverse("email-verification")

        absurl = "http://"+current_site+relative_link+"?token="+str(token)

        email_body = f"Hi {user.username} please use the link below to verify your email \n {absurl}"
        data = {
            "email_body": email_body, "to_email": user.email, "email_subject": "verify your email"
        }
        print(data)
        Util.send_email(data)

        return Response(user_data, status=status.HTTP_201_CREATED)


class verifyEmail(views.APIView):

    serializer_class = EmailVerificationSerializer
    renderer_classes = (UserRender, )

    token_param_config = openapi.Parameter(
        "token", in_=openapi.IN_QUERY, description='Description', type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[token_param_config])
    def get(self, request):
        token = request.GET.get("token")

        try:
            payload = jwt.decode(
                str(token), settings.SECRET_KEY, algorithms=['HS256'])
            user = User.objects.get(id=payload["user_id"])

            if not user.is_verified:
                user.is_verified = True
                user.save()

            return Response({"email": "successfully activated"}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError as identifier:
            return Response({"error": "Activation link expired"}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as identifier:
            return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(generics.GenericAPIView):

    serializer_class = LoginSerializer
    renderer_classes = (UserRender, )

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class RequestPasswordEmail(generics.GenericAPIView):

    serializer_class = RequestPasswordEmailSerializer
    renderer_classes = (UserRender, )

    def post(self, request):

        serializer = self.serializer_class(data=request.data)
        email = request.data["email"]

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))

            token = PasswordResetTokenGenerator().make_token(user)

            current_site = get_current_site(request=request).domain

            relative_link = reverse(
                "password-rest-confirm", kwargs={"uidb64": uidb64, "token": token})

            absurl = "http://"+current_site + relative_link

            email_body = f"Hello \n please use the link below to reset your password \n {absurl}"
            data = {
                "email_body": email_body, "to_email": user.email, "email_subject": "Reset your password"
            }
            print(data)
            Util.send_email(data)

        return Response({"success": "We have sent you a link to reset your password"}, status=status.HTTP_200_OK)


class PasswordTokenCheckAPI(generics.GenericAPIView):
    renderer_classes = (UserRender, )

    def get(self, request, uidb64, token):
        try:
            id = smart_str(urlsafe_base64_decode(uidb64))

            user = User.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({"error": "Token is not valid, Please request for a new one"}, status=status.HTTP_401_UNAUTHORIZED)

            return Response({"success": True, "message": "Crendential valid", "uidb64": uidb64, "token": token}, status=status.HTTP_200_OK)
        except DjangoUnicodeDecodeError as identifier:
            return Response({"error": "Token is not valid, Please request for a new one"}, status=status.HTTP_401_UNAUTHORIZED)


class SetNewPasswordAPIView(generics.GenericAPIView):

    serializer_class = SetNewPasswordSerializer
    renderer_classes = (UserRender, )

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response({"success": True, "message": "Password Reset success"}, status=status.HTTP_200_OK)
