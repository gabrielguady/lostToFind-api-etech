from rest_framework import routers
from core import viewsets

router = routers.DefaultRouter()
router.register('lost-items', viewsets.LostItemViewSet, basename='lost-items')
router.register('found-items', viewsets.FoundItemViewSet, basename='found-items')
router.register('categories', viewsets.CategoryViewSet, basename='categories')
router.register('file-images', viewsets.FileImageViewSet, basename='file-images')
router.register('comment', viewsets.CommentViewSet, basename='comment')
router.register('user', viewsets.UserViewSet, basename='user')

urlpatterns = router.urls