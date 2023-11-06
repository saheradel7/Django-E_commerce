from rest_framework import serializers
from django.contrib.auth.models import User

class SignuUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name' , 'email' , 'password')

        extra_Kwargs = {
            'first_name' :{'required':True , 'allow_blank':False}, 
            'last_name' :{'required':True , 'allow_blank':False},
            'email' :{'required':True , 'allow_blank':False},
            'password' :{'required':True , 'allow_blank':False, 'min_length': 5}
        }


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name' , 'email' , 'username')