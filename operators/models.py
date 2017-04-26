import datetime
from mongoengine import *
from django.utils.translation import ugettext as _

connect('paper_mailing')


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