from rest_framework import routers

from core import viewsets

router = routers.DefaultRouter()


router.register('lost_item', viewsets.LostItemViewSet)

router.register('found_item', viewsets.FoundItemViewSet)
router.register('category',viewsets.CategoryViewSet)
router.register('file_image', viewsets.FileImageViewSet)
router.register('user', viewsets.UserViewSet)
urlpatterns = router.urls