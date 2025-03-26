from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from users.serializers import UserRegisterSerializer, UserConfirmSerializer, UserAuthSerializer
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from users.models import ConfirmationCode
import random


@api_view(['POST'])
def authorization_api_view(request):
    serializer = UserAuthSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = authenticate(**serializer.validated_data)
    if user:
        token, _ = Token.objects.get_or_create(user=user)
        return Response(data={'token': token.key}, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
def registration_api_view(request):
    serializer = UserRegisterSerializer(data=request.data) 
    serializer.is_valid(raise_exception=True)

    username = serializer.validated_data.get('username')
    password = serializer.validated_data.get('password')

    user = User.objects.create_user(username=username, password=password, is_active=False)
    confirm = random.randint(100000, 999999)
    confirm = ConfirmationCode.objects.create(user=user, code=confirm)
    return Response(status=status.HTTP_201_CREATED, data = {'user_id': user.id})


@api_view(['POST'])
def confirm_api_view(request):
    if request.method == 'POST':
        if 'username' in request.data:
            user_id = User.objects.get(username=request.data['username']).id
            code = ConfirmationCode.objects.get(user_id=user_id).code
            return Response('Your confirmation code is {}'.format(code))
        elif 'code' in request.data:
            serializer = UserConfirmSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            code = serializer.validated_data.get('code')
            serializer.activate_user(code)
            return Response(status=status.HTTP_200_OK, data={'message':'Your account has been confirmed'})