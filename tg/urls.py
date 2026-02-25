from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import TgUserViewSet

router = DefaultRouter()
router.register(r"tg", TgUserViewSet, basename="tg")

urlpatterns = [
    path("", include(router.urls)),
]
