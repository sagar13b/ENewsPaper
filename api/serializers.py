from rest_framework import serializers
from editor.models import NewsPost
from account.models import User

class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsPost
        fields = '__all__'

class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('password',)

class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email','password')