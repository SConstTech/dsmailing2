from mongoengine import *
connect(db='app89', host='mongodb://jovial:kajimida1@ds135818.mlab.com:35818/app89')
# raise "Configure the MongoDB URI connection address"

# example ORM
class Tasks(DynamicDocument):
    title = StringField(max_length=200, required=True)
    isDone = BooleanField(default=False)

class Project(EmbeddedDocument):
    name = StringField(max_length=250, required=True)


class Client(DynamicDocument):
    name = StringField(required=True)
    bulstat = StringField(required=True)
    projects = EmbeddedDocumentListField('Project')

class Criteria(EmbeddedDocument):
    type = StringField()
    value = StringField()

class UndeliveryCause(Document):
    type = StringField()
    num_type = IntField()

class Letters(Document):
    project_id = EmbeddedDocumentField('Project')
    letter_data = EmbeddedDocumentListField('Criteria')
    undelivery = EmbeddedDocumentListField('UndeliveryCause')
