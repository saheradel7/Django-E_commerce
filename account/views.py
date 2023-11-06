from datetime import datetime, timedelta
from django.utils import timezone
from django.shortcuts import render
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status   
from .serializer import UserSerializer , SignuUpSerializer
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from rest_framework.response import Response
from django.utils.crypto import get_random_string
from django.shortcuts import get_object_or_404, render
from django.core.mail import send_mail

# Create your views here.


@api_view(['Post'])
def register(request):
    data = request.data
    user = SignuUpSerializer(data=data)
    if user.is_valid():
        if not User.objects.filter(username= data['email']).exists():
            user =User.objects.create(
                first_name = data['first_name'],
                last_name  = data['last_name'],
                email      = data['email'],
                username   = data['email'],
                password   = make_password(data['password'])
            )
            return Response({
            
                'details': 'user is registered',
                'Welcome Mr': user.first_name +' '+ user.last_name
            })
        else:
            return Response({'msg':'this user is exists'}, status=status.HTTP_400_BAD_REQUEST)
    return Response(user.errors)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user(request):
   
    user= UserSerializer(request.user)
    return Response(user.data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_user(request):
    user = request.user
    data = request.data

    user.first_name = data['first_name'],
    user.last_name = data['last_name'],
    user.email = data['email'],
    user.username = data['email'],
    if data['password'] != "":
        user.password = make_password(data['password'])

    user.save()
    ser = UserSerializer(user)
    return Response({"details":"user updated ", 'user':ser.data}, )

def get_current_host(request):
    protocol = request.is_secure() and 'https' or 'http'
    host = request.get_host()
    return "{protocol}://{host}/".format(protocol=protocol, host=host)

@api_view(['POST'])
def forgot_password(request):
    data = request.data

    user = get_object_or_404(User, email=data['email'])

    token = get_random_string(40)
    expire_date = datetime.now() + timedelta(minutes=1)

    user.profile.reset_password_token = token
    user.profile.reset_password_expire = expire_date

    user.profile.save()

    host = get_current_host(request)

    link = "{host}api/reset_password/{token}".format(host=host, token=token)
    body = "Your password reset link is: {link}".format(link=link)

    send_mail(
        "Password reset for eShop",
        body,
        "noreply@eshop.com",
        [data['email']]
    )

    return Response({ 'details': 'Password rest email sent to: {email}'.format(email=data['email']) })


@api_view(['POST'])
def reset_password(request, token):
    data = request.data

    user = get_object_or_404(User, profile__reset_password_token=token)

    if user.profile.reset_password_expire.replace(tzinfo=None) < datetime.now():
        return Response({ 'error': 'Token in expired' }, status=status.HTTP_400_BAD_REQUEST)


    if data['password'] != data['confirmPassword']:
        return Response({ 'error': 'Passwords are not same' }, status=status.HTTP_400_BAD_REQUEST)

    user.password = make_password(data['password'])
    user.profile.reset_password_token = ""
    user.profile.reset_password_expire = None

    user.profile.save()
    user.save()

    return Response({ 'details': 'Password reset successfully'})