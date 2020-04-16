from rest_framework import serializers
from mccr.models import MCCRRegistry, MCCRFile, MCCRRegistryOVVRelation, OVV

class MCCRFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = MCCRFile
        fields = ('id', 'file', 'user', 'mccr')

class OVVSerializer(serializers.ModelSerializer):

    class Meta:
        model = OVV
        fields = ('id', 'email', 'phone', 'name')


class MCCRRegistrySerializerView(serializers.ModelSerializer):
    files = MCCRFileSerializer(many=True)
    class Meta:
        model = MCCRRegistry
        fields = ('id', 'user', 'mitigation', 'user_type', 'fsm_state', 'files')

class MCCRRegistrySerializerCreate(serializers.ModelSerializer):
    class Meta:
        model = MCCRRegistry
        fields = ('id', 'user', 'mitigation', 'user_type', 'status')

class MCCRRegistryOVVRelationSerializer(serializers.ModelSerializer):
    class Meta:
        model = MCCRRegistryOVVRelation
        fields = ('id', 'mccr', 'ovv', 'status')