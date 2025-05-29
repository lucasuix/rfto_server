from django.urls import path, include
from rest_framework_mongoengine.routers import DefaultRouter
from .views import RftsViewSet

router = DefaultRouter()
router.register(r'rfts', RftsViewSet)

urlpatterns = [
    path('', include(router.urls)),
]