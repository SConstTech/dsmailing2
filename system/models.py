from mongoengine import *
connect('dsmailing-db')
from django.utils.translation import ugettext as _
# raise "Configure the MongoDB URI connection address"
from django.db import models
from django.contrib.auth.models import User

class Projects(DynamicDocument):
    name = StringField()

class Clients(DynamicDocument):
    name = StringField(required=True)
    projects = ListField(ReferenceField(Projects))

class Letters_values(DynamicEmbeddedDocument):
    name = StringField()
    value = StringField()

class Delivery(DynamicEmbeddedDocument):
    '''
    status:
        not-verified - неясно
        Delivered - доставено
        Undelivered - недоставено
    reason:
        Получателят отказва да получи пратката
        Пратката не е потърсена от получателя
        Получателят отсъства
        Получателят се е преместил на друг адрес
        Адресът вече не съществува
        Получателят непознат на посочения адрес
        Починал
        Непълен адрес на получателя

    '''

    status = StringField(default=_('Delivered'))
    reason = StringField()

class Letters(DynamicDocument):
    '''
    operatorMarked - operatorID marked it as not delivered

    '''
    value = ListField(EmbeddedDocumentField(Letters_values))
    # barcode = StringField(unique=True)
    status = ListField(EmbeddedDocumentField(Delivery))
    print_date = DateTimeField()
    status_date = DateTimeField()
    client = ReferenceField(Clients)
    operatorMarked = IntField()

    meta  ={
        'indexes': [
            'barcode'
        ]
    }
    # TODO: Fix the scoping
    # def find_letter(self, name, value):
    #     return self.value.get(value = value, name=name)


class basesImported(DynamicDocument):
    dateImported = DateTimeField()
    client = StringField()
    filename = StringField()

class clientUser(models.Model):
    '''
    role - user, superuser, boss ... something like that ... future TODO:
    '''
    user = models.OneToOneField(User,)
    office = models.CharField(max_length=500, default='')
    contact = models.CharField(max_length=500, default='')
    role = models.CharField(max_length=30, default='user')