from rest_framework import serializers
from mccr.models import MCCRRegistry, MCCRFile, MCCRRegistryOVVRelation

class MCCRFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = MCCRFile
        fields = ('id', 'file', 'user', 'mccr')


class MCCRRegistrySerializerView(serializers.ModelSerializer):
    files = MCCRFileSerializer(many=True)
    class Meta:
        model = MCCRRegistry
        fields = ('id', 'user', 'mitigation', 'user_type', 'status', 'files')

class MCCRRegistrySerializerCreate(serializers.ModelSerializer):
    class Meta:
        model = MCCRRegistry
        fields = ('id', 'user', 'mitigation', 'user_type', 'status')

class MCCRRegistryOVVRelationSerializer(serializers.ModelSerializer):
    class Meta:
        model = MCCRRegistryOVVRelation
        fields = ('id', 'mccr', 'ovv', 'status')