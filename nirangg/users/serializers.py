from rest_framework import serializers
from users.models import NirangUser


class UsersSerializer(serializers.ModelSerializer):
    email = serializers.CharField(required=True)

    class Meta:
        model = NirangUser
        fields = ('id', 'first_name', 'last_name', 'mobile', 'email', 'username', 'is_superuser')
