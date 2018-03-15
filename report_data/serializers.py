from rest_framework import serializers
from .models import ReportFile, ReportFileVersion


class ReportFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportFile
        fields = ('name', 'file', 'created', 'updated', 'versions')

class ReportFileVersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportFileVersion
        fields = ('version', 'active')
