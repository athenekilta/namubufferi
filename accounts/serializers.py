from rest_framework import serializers

from accounts.models import CustomUser

class UsernameSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('username', )