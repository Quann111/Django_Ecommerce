from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class UserSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(max_length=30)
    last_name = serializers.CharField(max_length=30)
    email = serializers.EmailField()
    # phone = serializers.CharField(max_length=15)
    

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email',]
