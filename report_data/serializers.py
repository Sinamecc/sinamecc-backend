from django.urls import reverse
from rest_framework import serializers
import report_data
from report_data.models import ReportData, Report, ReportFile, ReportDataChangeLog
from mitigation_action.serializers import ContactSerializer
from users.serializers import CustomUserSerializer


class ReportDataChangeLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportDataChangeLog
        fields = ('id', 'report_data', 'changes', 'change_description', 'author', 'updated')
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['author'] = CustomUserSerializer(instance.author).data

        return data


class ReportDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportData
        fields = ('__all__')
        
 
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['contact'] = ContactSerializer(instance.contact).data
        data['report_data_change_log'] = ReportDataChangeLogSerializer(instance.report_data_change_log.all().order_by('-id'), many=True).data
        data['files'] = ReportFileSerializer(instance.report_file.all(), many=True).data

        return data


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ('id', 'user', 'report_data', 'version', 'active')


class ReportFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportFile
        fields = ('id', 'slug', 'file', 'report_data', 'report_type')
        
    def _get_url(self, obj):
        
        return reverse('get_file_to_report_data', kwargs={'report_file_id': obj.id})
    
    
    def to_representation(self, instance):
        
        data =  super().to_representation(instance)
        data["file"] = self._get_url(instance)
        
        return data
