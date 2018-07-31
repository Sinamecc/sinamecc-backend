from rest_framework import serializers
from mitigation_action.ingei.models import HarmonizationIngei,HarmonizationIngeiFile
from mitigation_action.models import Mitigation

class HarmonizationIngeiSerializer(serializers.ModelSerializer):
    class Meta:
        model = HarmonizationIngei
        fields = ('user','name')

class HarmonizationIngeiFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = HarmonizationIngeiFile
        fields = ('user','mitigation_action','file','harmonization_ingei')

class HarmonizationSerializerView(serializers.ModelSerializer):
    class Meta:
        model = HarmonizationIngeiFile
        fields = ('id', 'user','name', 'mitigation_action', 'harmonization_ingei', 'files')