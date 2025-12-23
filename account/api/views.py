from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from account.api.serializer import UserRegistrationSerializer,UserLoginSerializer
from django.contrib.auth import authenticate

class UserRegistrationView(APIView):
    def post(self,request, format=None):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            return Response({"message":"Registration sucessfully"},status.HTTP_201_CREATED)
        return Response(serializer.errors, status.HTTP_422_UNPROCESSABLE_ENTITY)
    
class UserLoginView(APIView):
    def post(self,request, format=None):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data.get('email')
            password = serializer.data.get('password')
            user = authenticate(email=email, password=password)
            if user is not None:
                return Response({"message":"Login Sucess"}, status.HTTP_200_OK)
            else:
                return Response({'errors':{'non_field_errors':['Email or Password is not valid']}}, status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status.HTTP_422_UNPROCESSABLE_ENTITY)
        