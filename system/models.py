from mongoengine import *
connect('dsmailing-db')
from django.utils.translation import ugettext as _
# raise "Configure the MongoDB URI connection address"
from django.db import models
from django.contrib.auth.models import User

REQUEST_STATUS = (
    ('0', 'Очаква обработка'),
    ('1', 'В печат'),
    ('2', 'Очаква куриер'),
    ('3', 'Изпратена'),
    ('4', 'Очаква потвърждение от офис'),
)

# MONGODB CONNECTION FOR INCORRECT DELIVERY APP (EMILOV)


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

# END MONGODB DEFINITIONS

# POSTGRESQL DB DEFINITIONS FOR CUSTOMER REQUEST PROCESSING DATA

class clientUser(models.Model):
    '''
    role - user, superuser, boss ... something like that ... future TODO:
    '''
    user = models.OneToOneField(User,)
    delivery_address = models.CharField(max_length=500, default='')
    contact = models.CharField(max_length=500, default='')
    role = models.CharField(max_length=30, default='user')
    avatar = models.ImageField(upload_to='avatar/')


class CustomerProjects(models.Model):
    name = models.CharField(max_length=500)
    price_per_item = models.IntegerField()

class Customers(models.Model):
    name = models.CharField(max_length=500)
    projects_id = models.ForeignKey(CustomerProjects, null=True, related_name='customer_projects')
    legal_name = models.CharField(max_length=500)
    legal_address = models.CharField(max_length=700)
    legal_EIK = models.CharField(max_length=50)

class ItemType(models.Model):
    name = models.CharField(max_length=500)
    customer_id = models.ForeignKey(Customers, related_name='customer_items')
    project_id = models.ForeignKey(CustomerProjects, related_name='customer_project_items')

class clientRequest(models.Model):
    date_requested = models.DateTimeField(auto_now_add=True)
    date_processed = models.DateTimeField(null=True)
    status = models.CharField(max_length=150, choices=REQUEST_STATUS, default='0')
    request_file = models.FileField(upload_to='request_files/')
    completed = models.BooleanField(default=False)

class requestElement(models.Model):
    request_id = models.ForeignKey(clientRequest, related_name='request_element')
    item_type_id = models.ForeignKey(ItemType, related_name='sales_item')
    count = models.IntegerField()
