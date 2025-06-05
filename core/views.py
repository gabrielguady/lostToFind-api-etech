# from rest_framework import viewsets, permissions
# from core import models
# from . import serializers
#
# class LostItemViewSet(viewsets.ModelViewSet):
#     queryset = models.LostItem.objects.all()
#     serializer_class = serializers.LostItemSerializer
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly]
#
#     def get_serializer_context(self):
#         context = super().get_serializer_context()
#         context.update({"request": self.request})
#         return context
#
#
# class FoundItemViewSet(viewsets.ModelViewSet):
#     queryset = models.FoundItem.objects.all()
#     serializer_class = serializers.FoundItemSerializer
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly]
#
#     def get_serializer_context(self):
#         context = super().get_serializer_context()
#         context.update({"request": self.request})
#         return context
#
#
# class FileImageItemViewSet(viewsets.ModelViewSet):
#     queryset = models.FileImageItem.objects.all()
#     serializer_class = serializers.FileImageSerializer
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly]
#
#
# class CategoryItemViewSet(viewsets.ModelViewSet):
#     queryset = models.Category.objects.all()
#     serializer_class = serializers.CategoryItemSerializer
#     permission_classes = [permissions.AllowAny]
#
#
# class UserViewSet(viewsets.ModelViewSet):
#     queryset = models.User.objects.all()
#     serializer_class = serializers.UserSerializer
#     permission_classes = [permissions.AllowAny]
#
#     def get_serializer_context(self):
#         context = super().get_serializer_context()
#         context.update({"request": self.request})
#         return context
