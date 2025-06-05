from api.models import Rfts
from datetime import datetime
from api.serializers import RftsSerializer
from .calculate_time import WorkTimeCalculator
import logging

logger = logging.getLogger(__name__)

class ApiController:

    @staticmethod
    def saveandreturn(rft_serializer: RftsSerializer, affirmative_message: str , negative_message: str):
        if rft_serializer.is_valid():
            try:
                rft = rft_serializer.save()
                return {'success': True,
                        'toast': affirmative_message,
                        'rft': RftsSerializer(rft).data}
            except Exception as e:
                logger.error(f"Um erro ocorreu: {str(e)}")
        else:
            return {'success': False, 
                    'toast': negative_message, 
                    'erros': rft_serializer.errors}
    
    @staticmethod
    def run(rft_data, metadata):
        
        action = metadata['action']

        actions = {
        "nova_rft": ApiController.new_rft,
        "concluir_manutencao": ApiController.finish_maintenence,
        "iniciar_manutencao": ApiController.start_maintenence,
        "salvar_manutencao": ApiController.save_maintenence,
        "pausar_manutencao": ApiController.pause_maintenence,
        "retomar_manutencao": ApiController.unpause_maintenence
        }
        return actions[action](rft_data)
    
    @staticmethod
    def new_rft(rft_data):
        rft_serializer = RftsSerializer(data=rft_data)
        return ApiController.saveandreturn(rft_serializer, 
                                           'RFT criada com sucesso', 
                                           'Erro! Verifique os campos da RFT.')
    
    @staticmethod
    def finish_maintenence(rft_data):
        print(rft_data)
        rft = Rfts.objects.get(id=rft_data['id'])
        if rft:
            rft_data['concluida_em'] = datetime.now()
            old_metadata = rft.metadata.to_mongo().to_dict()
            old_metadata['duracao_real'] = WorkTimeCalculator.to_minutes(rft_data['concluida_em'] - rft.iniciada_em)
            old_metadata['duracao_propria'] = WorkTimeCalculator.calculate_total_minutes(rft.iniciada_em, rft_data['concluida_em']) - old_metadata['tempo_congelada']
            old_metadata['concluida'] = True
            rft_data['metadata'] = old_metadata
            rft_serializer = RftsSerializer(instance=rft, data=rft_data, partial=True)
            return ApiController.saveandreturn(rft_serializer,
                                               'RFT concluída com sucesso!',
                                               'Um erro ocorreu ao concluir a RFT')
        else:
            return {'success': False,
                    'toast': 'Nenhuma RFT foi encontrada para essa TCU!'}

    @staticmethod
    def save_maintenence(rft_data):
        print(rft_data)
        rft = Rfts.objects.get(id=rft_data['id'])
        if rft:
            rft_serializer = RftsSerializer(instance=rft, data=rft_data, partial=True)
            return ApiController.saveandreturn(rft_serializer,
                                               'Alterações salvas!',
                                               'Um erro ocorreu ao salvar a RFT')
        else:
            return {'success': False,
                    'toast': 'Nenhuma RFT foi encontrada para essa TCU!'}
    
    @staticmethod
    def start_maintenence(rft_data):
        rft = Rfts.objects(serialnumber=rft_data['serialnumber']).first()
        if rft:
            rft_data['iniciada_em'] = datetime.now()
            rft_serializer = RftsSerializer(instance=rft, data=rft_data, partial=True)
            return ApiController.saveandreturn(rft_serializer, 
                                               'Dados da RFT recuperados com sucesso!', 
                                               'Um erro ocorreu ao recuperar dados da RFT')
        else:
            return {'success': False,
                    'toast': 'Nenhuma RFT foi encontrada para essa TCU!'}
    
    @staticmethod
    def pause_maintenence(rft_data):
        print(rft_data)
        rft = Rfts.objects.get(id=rft_data['id'])
        if rft:
            old_metadata = rft.metadata.to_mongo().to_dict()  # Converte para dicionário puro
            old_metadata['congelada'] = True
            old_metadata['congelamento_inicio'] = datetime.now()
            old_metadata['tempo_congelada'] = 0
            rft_data['metadata'] = old_metadata
            rft_serializer = RftsSerializer(instance=rft, data=rft_data, partial=True)
            return ApiController.saveandreturn(rft_serializer,
                                               'RFT pausada! Só será possível concluir após retomar.',
                                               'Ocorreu um erro ao pausar RFT')
        else:
            return {'success': False,
                    'toast': 'Nenhuma RFT foi encontrada para essa TCU!'}

    @staticmethod
    def unpause_maintenence(rft_data):
        print(rft_data)
        rft = Rfts.objects.get(id=rft_data['id'])
        if rft:
            old_metadata = rft.metadata.to_mongo().to_dict()  # Converte para dicionário puro
            old_metadata['congelada'] = False
            old_metadata['congelamento_final'] = datetime.now()
            old_metadata['tempo_congelada'] = old_metadata['tempo_congelada'] + WorkTimeCalculator.calculate_total_minutes(old_metadata['congelamento_inicio'], old_metadata['congelamento_final'])
            rft_data['metadata'] = old_metadata
            rft_serializer = RftsSerializer(instance=rft, data=rft_data, partial=True)
            return ApiController.saveandreturn(rft_serializer,
                                               'RFT retomada com sucesso!',
                                               'Ocorreu um erro ao retomar RFT')
        else:
            return {'success': False,
                    'toast': 'Nenhuma RFT foi encontrada para essa TCU!'}
'''
{
            'success': True,
            'toast': 'Dados de RFT recuperados com sucesso',
            'rft': {
                'id': '82ydsycu389e98',
                'serialnumber': '0225030209090',
                'operador_id': '17',
                'tecnico_id': '17',
                'etapa_id': '1',
                'erro_id': '4',
                'enviada_em': datetime(2025, 4, 15, 7, 56),
                'iniciada_em': datetime(2025, 4, 15, 16, 30),
                'concluida_em': datetime(2025, 6, 4, 13, 20),
                'perdas': 'Capacitor C57',
                'defeitos': {
                    'burnin': 'TCU não comunica serialmente'
                },
                'metadata': { # Dados que não são mostrados para o usuário
                    'concluida': True,
                    'descricao_defeito': 'TCU não comunica',
                    'duracao_real': 400,
                    'duracao_propria': 180,
                    'tempo_congelada': 20, # Minutos
                    'congelada': True,
                    'congelamento_inicio': datetime(2025, 5, 27, 7, 40),
                    'congelamento_final': datetime(2025, 6, 3, 16, 40),
                    'rft_enviada': False,
                    'manutencao_enviada': False 
                }
            }
        }


'''
