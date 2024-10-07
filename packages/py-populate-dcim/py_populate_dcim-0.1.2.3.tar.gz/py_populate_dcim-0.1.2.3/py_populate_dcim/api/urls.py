# api/urls.py
from rest_framework import routers
from .views import RefreshRequestViewSet

router = routers.DefaultRouter()
router.register('refresh', RefreshRequestViewSet)
urlpatterns = router.urls
