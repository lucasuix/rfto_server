from django.urls import path, include
from rest_framework_mongoengine.routers import DefaultRouter
from .views import RftsViewSet, APP

router = DefaultRouter()
router.register(r'rfts', RftsViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('app/', APP.as_view(), name='rfts-acao')
]