from rest_framework import serializers
from report_data.models import ReportData, Report, ReportFile, ReportFileVersion



class ReportDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportData
        fields = '__all__'

class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ('id', 'user', 'report_data', 'version', 'active')

class ReportFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportFile
        fields = ('id', 'slug', 'report_file')


class ReportFileVersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportFileVersion
        fields = ('id', 'report_file', 'version', 'file')