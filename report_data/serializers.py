from rest_framework import serializers
from report_data.models import ReportFile, ReportFileVersion


class ReportFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportFile
        fields = ('id', 'user', 'name', 'created', 'updated')

class ReportFileVersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportFileVersion
        fields = ('version', 'active', 'file', 'report_file', 'user')
