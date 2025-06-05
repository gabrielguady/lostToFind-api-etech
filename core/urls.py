from rest_framework import routers
from core.viewsets import (
    LostItemViewSet,
    FoundItemViewSet,
    CategoryViewSet,
    FileImageViewSet,
    UserViewSet
)

router = routers.DefaultRouter()
router.register('lost-items', LostItemViewSet, basename='lost-items')
router.register('found-items', FoundItemViewSet, basename='found-items')
router.register('categories', CategoryViewSet, basename='categories')
router.register('file-images', FileImageViewSet, basename='file-images')
router.register('user', UserViewSet, basename='user')

urlpatterns = router.urls