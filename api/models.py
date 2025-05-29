# from django.db import models
from mongoengine import *
from datetime import datetime
# Create your models here.

connect('rft_db')

class Rfts(Document):
    # Envio
    serialNumber = StringField(regex=r'^\d{1,13}$', required=True)
    operadorID = StringField(required=True)
    stage = StringField(required=True, choices=['burnin', 'pre_tests', 'potencia'])
    defect = DictField(required=True)
    sent_in = DateTimeField(default=datetime.now(), required=True)
    obs = StringField(required= False)
    status = StringField(required=True, choices=['concluida', 'aberta'], default='aberta')

    # Manutenção
    start_time = DateTimeField()
    end_time = DateTimeField()
    tecnicoID = StringField()
    actions_taken = StringField(max_length=200)
    solucao = StringField()
    rft_id = StringField()



    
