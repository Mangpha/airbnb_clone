# DRF Imports
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, exceptions
from rest_framework.permissions import IsAuthenticated

# Serializer Imports
from . import serializers as user_serial

# Model Imports


class Me(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(user_serial.PrivateUserSerializer(request.user).data)

    def put(self, request):
        serializer = user_serial.PrivateUserSerializer(
            request.user,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            user = serializer.save()
            serializer = user_serial.PrivateUserSerializer(user)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class Users(APIView):

    def post(self, request):
        password = request.data.get("password")
        if not password:
            raise exceptions.ParseError
        serializer = user_serial.PrivateUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.set_password(password)
            user.save()
            serializer = user_serial.PrivateUserSerializer(user)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
