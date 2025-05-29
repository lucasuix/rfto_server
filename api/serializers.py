from rest_framework_mongoengine.serializers import DocumentSerializer
from rest_framework_mongoengine.serializers import serializers
from .models import Rfts

class RftsSerializer(DocumentSerializer):
    # rft_id =  serializers.DictField(required=False, allow_null=True)

    class Meta:
        model = Rfts
        fields = '__all__'