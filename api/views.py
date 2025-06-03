from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_mongoengine.viewsets import ModelViewSet
from .models import Rfts
from .serializers import RftsSerializer
from .modules.apicontroller import ApiController

# Create your views here.
class RftsViewSet(ModelViewSet):
    lookup_field = 'id'
    serializer_class = RftsSerializer
    queryset = Rfts.objects.all()

class APP(APIView):

    def post(self, request):

        rft_data = dict(request.data['rft'])
        metadata = dict(request.data['metadata'])
        
        response = ApiController.run(rft_data, metadata)
        return Response(response, status=status.HTTP_200_OK)
