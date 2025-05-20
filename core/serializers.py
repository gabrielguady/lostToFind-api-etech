from rest_framework import serializers
from core import models
from core.models import User

class FileImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.FileImageItem
        fields = '__all__'

class LostItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.LostItem
        fields = '__all__'

class FoundItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.FoundItem
        fields = '__all__'

class CategoryItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = '__all__'

