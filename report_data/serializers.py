from django.urls import reverse
from rest_framework import serializers
from report_data.models import ChangeLog, ReportData, Report, ReportFile, ReportDataChangeLog
from mitigation_action.serializers import ContactSerializer, ClassifierSerializer, ThematicCategorizationTypeSerializer, InformationSourceTypeSerializer
from users.serializers import CustomUserSerializer
from workflow.serializers import CommentSerializer
from report_data.workflow_steps.fsm_utils.fsm_states import RD_FSM_STATE
from general.utils import get_translation_from_database as _


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
            'label':  _(RD_FSM_STATE.get(instance.fsm_state), 'label'),
        }
        return data
    
    def _next_action(self, instance):
        
        transitions = instance.get_available_fsm_state_transitions()
        result = [
                    {
                        'state':transition.target,
                        'label': _(RD_FSM_STATE.get(transition.target), 'label'),
                        'required_comments': True
                    } for transition in transitions
                ]
        return result
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['fsm_state'] = self._get_fsm_state_info(instance)
        data['contact'] = ContactSerializer(instance.contact).data
        data['classifier'] = ClassifierSerializer(instance.classifier.all(), many=True).data
        data['information_source'] = InformationSourceTypeSerializer(instance.information_source.all(), many=True).data
        data['data_type'] = ThematicCategorizationTypeSerializer(instance.data_type).data
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
        fields = ('id', 'slug', 'filename', 'file', 'report_data', 'report_type')
        kwargs = {
            'filename': {'read_only': True},   
        }
        
    def _get_url(self, obj):
        
        return reverse('get_file_to_report_data', kwargs={'report_file_id': obj.id})
    
    
    def to_representation(self, instance):
        
        data =  super().to_representation(instance)
        data["file"] = self._get_url(instance)
        if not instance.filename:
            data["filename"] = instance.file.name.split('/')[-1]
        
        return data


class ChangeLogSerializer(serializers.ModelSerializer):

    class Meta:
        model = ChangeLog
        fields = ('id', 'date', 'report_data', 'previous_status', 'current_status', 'user')
