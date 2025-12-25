from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from account.api.serializer import (
    UserRegistrationSerializer,UserLoginSerializer,
    UserProfileSerializer,UserChangePasswordSerializer,SendPasswordRestEmailSerializer)
from django.contrib.auth import authenticate
from account.api.renderers import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated

def get_tokens_for_user(user):
    if not user.is_active:
      raise AuthenticationFailed("User is not active")
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class UserRegistrationView(APIView):
    renderer_classes = [UserRenderer]
    def post(self,request, format=None):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            token = get_tokens_for_user(user)
            return Response({"token":token, "message":"Registration sucessfully"},status.HTTP_201_CREATED)
        return Response(serializer.errors, status.HTTP_422_UNPROCESSABLE_ENTITY)
    
class UserLoginView(APIView):
    renderer_classes = [UserRenderer]
    def post(self,request, format=None):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data.get('email')
            password = serializer.data.get('password')
            user = authenticate(email=email, password=password)
            if user is not None:
                token = get_tokens_for_user(user)
                return Response({"token":token, "message":"Login Sucess"}, status.HTTP_200_OK)
            else:
                return Response({'errors':{'non_field_errors':['Email or Password is not valid']}}, status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status.HTTP_422_UNPROCESSABLE_ENTITY)
   
class UserProfileView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    def get(self,request,format=None):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data, status.HTTP_200_OK)

class UserChangePasswordView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    def post(self,request,format=None):
        serializer = UserChangePasswordSerializer(data=request.data, context={'user':request.user})
        if serializer.is_valid(raise_exception=True):
            return Response({"message":"Password Changed Sucessfully"},status.HTTP_200_OK)
        return Response(serializer.errors,status.HTTP_422_UNPROCESSABLE_ENTITY)
    
class SendPasswordResetEmailView(APIView):
    renderer_classes = [UserRenderer]
    def post(self,request,format=None):
        serializer = SendPasswordRestEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({"message":"password reset link send.Please check your email"},status.HTTP_200_OK)