from rest_framework_mongoengine.serializers import DocumentSerializer
from .models import Rfts

class RftsSerializer(DocumentSerializer):

    class Meta:
        model = Rfts
        fields = '__all__'

class ManutencaoSerializer(RftsSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make these fields required
        self.fields['tecnico_id'].required = True
        self.fields['solucao_id'].required = True
        self.fields['procedimento'].required = True
        self.fields['rft_id'].required = True

rft_serializer = RftsSerializer()
manutencao_serializer = ManutencaoSerializer()