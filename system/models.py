from mongoengine import *
connect('dsmailing-db')
from django.utils.translation import ugettext as _
# raise "Configure the MongoDB URI connection address"


class Projects(DynamicDocument):
    name = StringField()


class Clients(DynamicDocument):
    name = StringField(required=True)
    projects = ListField(ReferenceField(Projects))


class Letters_values(DynamicEmbeddedDocument):
    name = StringField()
    value = StringField()


class Letters(DynamicDocument):
    '''
    Delivered - доставено

    '''
    value = ListField(EmbeddedDocumentField(Letters_values))
    status = StringField(default=_('Delivered'))
    print_date = DateTimeField()
    status_date = DateTimeField()
    client = ReferenceField(Clients)


# # example ORM
# class Tasks(DynamicDocument):
#     title = StringField(max_length=200, required=True)
#     isDone = BooleanField(default=False)
#
# class Project(EmbeddedDocument):
#     name = StringField(max_length=250, required=True)
#
#
# class Client(DynamicDocument):
#     name = StringField(required=True)
#     bulstat = StringField(required=True)
#     projects = EmbeddedDocumentListField('Project')
#
# class Criteria(EmbeddedDocument):
#     type = StringField()
#     value = StringField()
#
# class UndeliveryCause(Document):
#     type = StringField()
#     num_type = IntField()
#
# class Letters(Document):
#     project_id = EmbeddedDocumentField('Project')
#     letter_data = EmbeddedDocumentListField('Criteria')
#     undelivery = EmbeddedDocumentListField('UndeliveryCause')


