from api.models import Rfts
from datetime import datetime
from api.serializers import RftsSerializer, ManutencaoSerializer
from .translator import Translator
from .tecsciserver import server

class ApiController:
    
    @staticmethod
    def run(rft_data, metadata):
        
        action = metadata['action']

        actions = {
        "nova_rft": ApiController.new_rft,
        "concluir_manutencao": ApiController.finish_maintenence,
        "iniciar_manutencao": ApiController.start_maintenence,
        "salvar_manutencao": ApiController.save_maintenence,
        }
        return actions[action](rft_data)
    
    @staticmethod
    def new_rft(rft_data):
        print(rft_data)
        return {'success': True, 'toast': 'RFT criada com sucesso!'}

        '''
        json_data["start_time"] = datetime.now()
        serializer = RftsSerializer(data=json_data)
        if serializer.is_valid():
            rft = serializer.save()

            #TECSCI INICIO
            tecsci_rft = Translator.mount_rft(rft)
            server.post_request("rft", tecsci_rft)
            #TECSCI FIM

            print(f"RFT criada com sucesso, ID: {rft.id}")
            return {"toast": "RFT cadastrada com sucesso!"}
        else:
            print(serializer.errors)
            return {"toast": "RFT possui dados inválidos."}
        '''
    
    @staticmethod
    def finish_maintenence(json_data): # Enviar o serialNumber, puxar a mais recente e montar a manutenção
        rft = Rfts.objects.get(id=json_data['id'])

        json_data["end_time"] = datetime.now()

        rfts = server.get_request("rft")
        rft_match = next((r for r in rfts if r['controladora_id'] == rft.serialNumber), None)
        json_data["rft_id"] = rft_match["id"]

        serializer = ManutencaoSerializer(rft, data=json_data, partial=True)
        if serializer.is_valid():
            rft = serializer.save()

            #TECSCI INICIO
            tecsci_manutencao = Translator.mount_manutencao(rft)
            server.post_request("manutencao", tecsci_manutencao)
            #TECSCI FIM

            print(f"RFT {rft.id} concluída com sucesso")
            return {"toast": "RFT concluída com sucesso"}
        else:
            print(serializer.errors)
            return {"toast": "RFT com campos faltando"}


    @staticmethod
    def save_maintenence(json_data):
        rft = Rfts.objects.get(id=json_data['id'])

        serializer = RftsSerializer(rft, data=json_data, partial=True)
        if serializer.is_valid():
            rft = serializer.save()
            print(f"RFT {rft.id} atualizada com {json_data}")
            return {"toast": "Alterações salvas"}
        else:
            print(serializer.errors)
            print(f"Erro ao salvar RFT {rft.id}")
            return {"toast": "Um erro ocorreu ao atualizar a RFT"}
    
    @staticmethod
    def start_maintenence(json_data):
        rft = Rfts.objects(serialNumber=json_data["serialNumber"]).order_by('-id').first()

        update_data = {
            "start_time": datetime.now()
        }

        serializer = RftsSerializer(rft, data=update_data, partial=True)
        if serializer.is_valid():
            rft = serializer.save()
            print(f"RFT {rft.id} atualizada com {update_data}")
            return {"rft": rft}
        else:
            print(f"Não encontrou nenhuma RFT para essa TCU {json_data["serialNumber"]}")
            return {"toast": "Não foi encontrada nenhuma RFT para essa TCU"}