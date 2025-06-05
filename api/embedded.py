from mongoengine import *
from datetime import datetime

connect('rft_db')

class MetaInfo(EmbeddedDocument):
    concluida = BooleanField(default=False)
    descricao_defeito = StringField()
    duracao_real = FloatField()
    duracao_propria = FloatField()
    tempo_congelada = FloatField(default=0)
    congelada = BooleanField(default=False)
    congelamento_inicio = DateTimeField()
    congelamento_final = DateTimeField()
    hora_extra = FloatField()
    hora_extra_inicio = DateTimeField()
    hora_extra_final = DateTimeField()
    rft_enviada = BooleanField(default=False)
    manutencao_enviada = BooleanField(default=False)
    perdas_enviadas = BooleanField(default=False)