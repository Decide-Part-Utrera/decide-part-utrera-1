from rest_framework import serializers
import os
from rest_framework.exceptions import AuthenticationFailed

from django.contrib.auth.models import User


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'is_staff')
