# from django.shortcuts import render
from rest_framework_mongoengine.viewsets import ModelViewSet
from .models import Rfts
from .serializers import RftsSerializer

# Create your views here.
class RftsViewSet(ModelViewSet):
    lookup_field = 'id'
    serializer_class = RftsSerializer
    queryset = Rfts.objects.all()