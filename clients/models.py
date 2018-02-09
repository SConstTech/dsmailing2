from mongoengine import *
connect('dsmailing-db')
# raise "Configure the MongoDB URI connection address"

class AddedDocuments(DynamicEmbeddedDocument):
    document_number = StringField()
    date_arrived = DateTimeField()
    checked = BooleanField(default=False)

class DocumentRequests(DynamicDocument):
    number_office = StringField()
    date_created = DateTimeField()
    documents_added = EmbeddedDocumentListField(AddedDocuments)
    finished_request = BooleanField(default=False)

