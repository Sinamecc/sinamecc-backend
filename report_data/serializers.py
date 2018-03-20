from rest_framework import serializers
from .models import ReportFile, ReportFileVersion


class ReportFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportFile
        fields = ('name', 'created', 'updated')

class ReportFileVersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportFileVersion
        fields = ('version', 'active', 'file')
