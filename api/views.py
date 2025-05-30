from rest_framework.views import APIView
from rest_framework.views import Response
from rest_framework import status
from rest_framework_mongoengine.viewsets import ModelViewSet
from .models import Rfts
from .serializers import RftsSerializer
from modules.apicontroller import ApiController

# Create your views here.
class RftsViewSet(ModelViewSet):
    lookup_field = 'id'
    serializer_class = RftsSerializer
    queryset = Rfts.objects.all()

class APP(APIView):

    def post(request):

        data = dict(request.data)
        action = data.pop('action')
        
        response = ApiController.run(data, action)
        return Response(response, status=status.HTTP_200_OK)