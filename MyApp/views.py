from django.shortcuts import redirect
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_201_CREATED
from .models import User
from .serializers import RegisterUserSerializer, UserLoginSerializer, UserLogoutSerializer, TokenExchangeSerializer, GetTransactionsSerializer, GetAccountSerializer, TransactionUpdateSerializer


class RegisterUser(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterUserSerializer


class Login(generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserLoginSerializer

    def post(self, request):
        serializer_class = UserLoginSerializer(data=request.data)
        if serializer_class.is_valid(raise_exception=True):
            return Response(serializer_class.data, status=HTTP_200_OK)
        return Response(serializer_class.errors, status=HTTP_400_BAD_REQUEST)


class Logout(generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserLogoutSerializer

    def post(self, request):
        serializer_class = UserLogoutSerializer(data=request.data)
        if serializer_class.is_valid(raise_exception=True):
            return Response(serializer_class.data, status=HTTP_200_OK)
        return Response(serializer_class.errors, status=HTTP_400_BAD_REQUEST)


class TokenExchange(generics.GenericAPIView):
    serializer_class = TokenExchangeSerializer

    def get(self, request):
        serializer_class = TokenExchangeSerializer(data=request.data)
        if serializer_class.is_valid(raise_exception=True):
            return Response(serializer_class.data, status=HTTP_200_OK)
        return Response(serializer_class.errors, status=HTTP_400_BAD_REQUEST)


class GetTransactions(generics.GenericAPIView):
    serializer_class = GetTransactionsSerializer

    def get(self, request):
        serializer_class = GetTransactionsSerializer(data=request.data)
        if serializer_class.is_valid(raise_exception=True):
            return Response(serializer_class.data, status=HTTP_200_OK)
        return Response(serializer_class.errors, status=HTTP_400_BAD_REQUEST)


class GetAccounts(generics.GenericAPIView):
    serializer_class = GetAccountSerializer

    def get(self, request):
        serializer_class = GetAccountSerializer(data=request.data)
        if serializer_class.is_valid(raise_exception=True):
            return Response(serializer_class.data, status=HTTP_200_OK)
        return Response(serializer_class.errors, status=HTTP_400_BAD_REQUEST)


class TransactionUpdate(generics.GenericAPIView):
    serializer_class = TransactionUpdateSerializer

    def post(self, request):
        serializer_class = TransactionUpdateSerializer(data=request.data)
        if serializer_class.is_valid(raise_exception=True):
            return Response(serializer_class.data, status=HTTP_200_OK)
        return Response(serializer_class.errors, status=HTTP_400_BAD_REQUEST)
