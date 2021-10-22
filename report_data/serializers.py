from rest_framework import serializers
from report_data.models import ReportFile, ReportFileVersion, ReportFileMetadata


class ReportFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportFile
        fields = ('id', 'user', 'name', 'contact', 'created', 'updated')

class ReportFileVersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportFileVersion
        fields = ('version', 'active', 'file', 'report_file', 'user')

class ReportFileMetadataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportFileMetadata
        fields = ('name','value','report_file')
