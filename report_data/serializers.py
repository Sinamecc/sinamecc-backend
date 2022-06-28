from django.urls import reverse
from rest_framework import serializers
import report_data
from report_data.models import ChangeLog, ReportData, Report, ReportFile, ReportDataChangeLog
from mitigation_action.serializers import ContactSerializer
from users.serializers import CustomUserSerializer
from workflow.serializers import CommentSerializer


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
        fields = ('id', 'fsm_state', 'user', 'name', 'description', 'unit', 'calculation_methodology', 'measurement_frequency', 'measurement_frequency_other', 
                  'from_date', 'to_date', 'geographic_coverage', 'geographic_coverage_other', 'disaggregation', 'limitation', 'additional_information', 'sustainable', 'responsible_institution', 
                  'information_source', 'statistical_operation', 'contact','contact_annotation', 'data_type', 'other_data_type', 'classifier', 'other_classifier', 
                  'report_information', 'have_base_line', 'base_line_type', 'base_line_report', 'have_quality_element', 'quality_element_description', 'transfer_data_with_sinamecc', 
                  'transfer_data_with_sinamecc_description', 'report_data_type', 'individual_report_data','review_count', 'comments', 'created', 'updated')
        
    def _get_fsm_state_info(self, instance):
        
        data = {
            'state': instance.fsm_state,
            'label':  f'{instance.fsm_state} label'
        }
        return data
    
    def _next_action(self, instance):
        
        transitions = instance.get_available_fsm_state_transitions()
        result = [
                    {
                        'state':transition.target, 
                        'label': f'{transition.target} label', 
                        'required_comments': True
                    } for transition in transitions
                ]
        return result
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['fsm_state'] = self._get_fsm_state_info(instance)
        data['contact'] = ContactSerializer(instance.contact).data
        data['report_data_change_log'] = ReportDataChangeLogSerializer(instance.report_data_change_log.all().order_by('-id'), many=True).data
        data['files'] = ReportFileSerializer(instance.report_file.all(), many=True).data
        data['comments'] = CommentSerializer(instance.comments.filter(fsm_state=instance.fsm_state, review_number=instance.review_count), many=True).data
        data['next_action'] = self._next_action(instance)

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


class ChangeLogSerializer(serializers.ModelSerializer):

    class Meta:
        model = ChangeLog
        fields = ('id', 'date', 'report_data', 'previous_status', 'current_status', 'user')
