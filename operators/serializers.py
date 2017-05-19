from operators.serializers import *
from rest_framework import serializers


class ProjectsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Projects
        fields = ('name')

class ClientsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Clients

class Letters_valuesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Letters_values

class LettersSerializer(DynamicDocument):
    class Meta:
        model = Letters