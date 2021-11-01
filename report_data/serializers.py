from rest_framework import serializers
from report_data.models import ReportData, Report, ReportFile, ReportFileVersion, ReportDataChangeLog
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
        fields = ('id', 'user', 'name', 'description', 'source', 'source_file', 'data_type', 'other_data_type', 
            'classifier', 'other_classifier', 'report_information', 'have_line_base', 'have_quality_element', 
            'quality_element_description', 'transfer_data_with_sinamecc', 'transfer_data_with_sinamecc_description', 
            'contact')
        
            
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['contact'] = ContactSerializer(instance.contact).data
        data['report_data_change_log'] = ReportDataChangeLogSerializer(instance.report_data_change_log.all().order_by('-id'), many=True).data

        return data


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

    