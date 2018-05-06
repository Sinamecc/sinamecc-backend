from rest_framework import serializers
from mccr.models import MCCRRegistry, MCCRFile


class MCCRRegistrySerializer(serializers.ModelSerializer):
    class Meta:
        model = MCCRRegistry
        fields = ('id', 'user', 'mitigation', 'user_type', 'status')

class MCCRFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = MCCRFile
        fields = ('id', 'file', 'user', 'mccr')