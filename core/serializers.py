from rest_flex_fields import FlexFieldsModelSerializer
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from core import models


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Adicione campos extras ao token aqui:
        token['username'] = user.username

        return token


class FileImageSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = models.FileImageItem
        fields = '__all__'


class LostItemSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = models.LostItem
        fields = '__all__'

    expandable_fields = {
        'user': (
            'core.UserSerializer',
            {'fields': ['id', 'first_name', 'last_name', 'email']},
        ),
        'category': (
            'core.CategorySerializer',
            {'fields': ['id', 'name']},
        ),
    }


class FoundItemSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = models.FoundItem
        fields = '__all__'

    expandable_fields = {
        'user': (
            'core.UserSerializer',
            {'fields': ['id', 'first_name', 'last_name', 'email']},
        ),
        'category': (
            'core.CategorySerializer',
            {'fields': ['id', 'name']},
        ),
    }


class CategorySerializer(FlexFieldsModelSerializer):
    class Meta:
        model = models.Category
        fields = '__all__'


class CommentSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = models.Comment
        fields = '__all__'

    expandable_fields = {
        'user': (
            'core.UserSerializer',
            {'fields': ['id', 'first_name', 'last_name', 'email']},
        ),
        'comments': (
            'core.CommentSerializer',
            {'many': True, 'fields': ['id', 'user', 'date_created', 'description']},
        ),
    }


class UserSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = models.User
        fields = '__all__'

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = models.User(**validated_data)
        user.set_password(password)
        user.save()
        return user
