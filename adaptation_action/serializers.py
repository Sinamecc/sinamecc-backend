
from django.db import models
from django.db.models import fields
from adaptation_action.workflow_steps.fsm_utils.fsm_states import AA_FSM_STATE
from general.helpers.serializer import SerializersHelper
from rest_framework import serializers
from django.conf import settings
from general.utils import get_translation_from_database as _
from django.urls import reverse

from adaptation_action.models import ODS, AdaptationAction, AdaptationActionInformation, AdaptationAxisGuideline, AdaptationActionType, AdaptationAxis, ChangeLog, ClimateThreat, \
     FinanceAdaptation, FinanceSourceType, FinanceStatus, Implementation, IndicatorAdaptation, InformationSource, InformationSourceType, Instrument, Mideplan, \
         NDCArea, NDCContribution, ReportOrganization, ReportOrganizationType, ThematicCategorizationType, Topics, SubTopics, Activity, TypeClimateThreat, \
             Classifier, ProgressLog, IndicatorSource, IndicatorMonitoring, GeneralReport, GeneralImpact, TemporalityImpact, ActionImpact, FinanceInstrument, Contact

from general.serializers import AddressSerializer

from workflow.serializers import CommentSerializer

class ReportOrganizationTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = ReportOrganizationType
        fields = ('id', 'code', 'entity_type', 'created', 'updated')

class ContactSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Contact
        fields = ('id', 'contact_position', 'contact_name', 'address', 'email', 'institution', 'phone')

class ReportOrganizationSerializer(serializers.ModelSerializer):

    class Meta:
        model = ReportOrganization
        fields = ('id', 'responsible_entity', 'legal_identification', 'elaboration_date', 'entity_address', 'report_organization_type', 'other_report_organization_type','contact', 'created', 'updated')

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['report_organization_type'] = ReportOrganizationTypeSerializer(instance.report_organization_type).data
        data['contact'] = ContactSerializer(instance.contact).data

        return data

class AdaptationActionTypeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = AdaptationActionType
        fields = ('id', 'name', 'code', 'created', 'updated')

class ODSSerializer(serializers.ModelSerializer):

    class Meta:
        model = ODS
        fields = ('id', 'code', 'name', 'created', 'updated')

class AdaptationActionInformationSerializer(serializers.ModelSerializer):

    class Meta:
        model = AdaptationActionInformation
        fields = ('id', 'name', 'objective', 'description', 'meta', 'adaptation_action_type', 'ods', 'created', 'updated')

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['adaptation_action_type'] = AdaptationActionTypeSerializer(instance.adaptation_action_type).data
        data['ods'] = ODSSerializer(instance.ods.all(), many = True).data

        return data

class TopicsSerializer(serializers.ModelSerializer):

    description = serializers.SerializerMethodField()
    
    class Meta:
        model = Topics
        fields = ('id', 'code', 'description', 'created', 'updated')

    def get_description(self, instance):
        return _(instance, 'description')

class SubTopicsSerializer(serializers.ModelSerializer):

    description = serializers.SerializerMethodField()

    class Meta:
        model = SubTopics
        fields = ('id', 'code', 'description', 'topic', 'created', 'updated')
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['topic'] = TopicsSerializer(instance.topic).data

        return data

    def get_description(self, instance):
        return _(instance, 'description')

class AdaptationAxisSerializer(serializers.ModelSerializer):

    description = serializers.SerializerMethodField()

    class Meta:
        model = AdaptationAxis
        fields = ('id', 'code', 'description', 'created', 'updated')

    def get_description(self, instance):
        return _(instance, 'description')

class AdaptationAxisGuidelineSerializer(serializers.ModelSerializer):

    description = serializers.SerializerMethodField()

    class Meta:
        model = AdaptationAxisGuideline
        fields = ('id', 'code', 'description','adaptation_axis', 'created', 'updated')
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['adaptation_axis'] = AdaptationAxisSerializer(instance.adaptation_axis).data

        return data
    
    def get_description(self, instance):
        return _(instance, 'description')

class NDCAreaSerializer(serializers.ModelSerializer):

    description = serializers.SerializerMethodField()

    class Meta:
        model = NDCArea
        fields = ('id', 'code', 'description', 'created', 'updated')

    def get_description(self, instance):
        return _(instance, 'description')

class NDCContributionSerializer(serializers.ModelSerializer):

    description = serializers.SerializerMethodField()

    class Meta:
        model = NDCContribution
        fields = ('id', 'code', 'description', 'ndc_area', 'created', 'updated')
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['ndc_area'] = NDCAreaSerializer(instance.ndc_area).data

        return data
    
    def get_description(self, instance):
        return _(instance, 'description')

class ActivitySerializer(serializers.ModelSerializer):

    description = serializers.SerializerMethodField()
    
    class Meta:
        model = Activity
        fields = ('id', 'code', 'description', 'sub_topic', 'ndc_contribution', 'adaptation_axis_guideline', 'created', 'updated')

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['sub_topic'] = SubTopicsSerializer(instance.sub_topic).data
        data['ndc_contribution'] = NDCContributionSerializer(instance.ndc_contribution.all(), many=True).data
        data['adaptation_axis_guideline'] = AdaptationAxisGuidelineSerializer(instance.adaptation_axis_guideline).data

        return data
    
    def get_description(self, instance):
        return _(instance, 'description')

class InstrumentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Instrument
        fields = ('id', 'name', 'created', 'updated')

class TypeClimateThreatSerializer(serializers.ModelSerializer):

    class Meta:
        model = TypeClimateThreat
        fields = ('id', 'code', 'name', 'created', 'updated')

class ClimateThreatSerializer(serializers.ModelSerializer):

    class Meta:
        model = ClimateThreat
        fields = ('id', 'type_climate_threat', 'other_type_climate_threat', 'description_climate_threat', 'vulnerability_climate_threat', 'exposed_elements', 'file_description_climate_threat', 'file_vulnerability_climate_threat', 'file_exposed_elements')
    
    def _get_url(self, obj, file_name):
        
        return reverse('get_file_to_adaptation_action', kwargs={'model_id': obj.id, 'file_name': file_name})

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['type_climate_threat'] = TypeClimateThreatSerializer(instance.type_climate_threat.all(), many=True).data
        data['file_description_climate_threat'] = self._get_url(instance, 'file_description_climate_threat')
        data['file_vulnerability_climate_threat'] = self._get_url(instance, 'file_vulnerability_climate_threat')
        data['file_exposed_elements'] = self._get_url(instance, 'file_exposed_elements')

        return data

class ImplementationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Implementation
        fields = ('id', 'start_date', 'end_date', 'responsible_entity', 'other_entity', 'action_code')

#Serializer section 3-4

class FinanceStatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = FinanceStatus
        fields = ('id', 'name', 'code', 'created', 'updated')

class FinanceSourceTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = FinanceSourceType
        fields = ('id', 'name', 'code', 'created', 'updated')

class FinanceInstrumentSerializer(serializers.ModelSerializer):

    class Meta:
        model = FinanceInstrument
        fields = ('id', 'name', 'code', 'created', 'updated')

class MideplanSerializer(serializers.ModelSerializer):

    class Meta:
        model = Mideplan
        fields = ('id', 'registry', 'name', 'entity', 'created', 'updated')

class StatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = FinanceStatus
        fields = ('id', 'name', 'code', 'created', 'updated')

class InformationSourceSerializer(serializers.ModelSerializer):

    class Meta:
        model = InformationSource
        fields = ('id', 'responsible_insttution', 'type_information', 'other_type', 'statistical_operation', 'created', 'updated')

class GeneralImpactSerializer(serializers.ModelSerializer):

    class Meta:
        model = GeneralImpact
        fields = ('id', 'name', 'code', 'created', 'updated')

class FinanceSerializer(serializers.ModelSerializer):

    class Meta:
        model = FinanceAdaptation
        fields = ('id', 'administration', 'budget', 'currency', 'year','status', 'source', 'finance_instrument', 'instrument_name', 'mideplan', 'created', 'updated')

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['status'] = FinanceStatusSerializer(instance.status).data
        data['source'] = FinanceSourceTypeSerializer(instance.source.all(), many=True).data
        data['finance_instrument'] = FinanceInstrumentSerializer(instance.finance_instrument.all(), many=True).data
        data['mideplan'] = MideplanSerializer(instance.mideplan).data
    
        return data

class InformationSourceTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = InformationSourceType
        fields = ('id', 'name', 'code', 'created', 'updated')

class InformationSourceSerializer(serializers.ModelSerializer):

    class Meta:
        model = InformationSource
        fields = ('id', 'responsible_institution', 'type_information', 'other_type', 'statistical_operation', 'created', 'updated')
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['type_information'] = InformationSourceTypeSerializer(instance.type_information.all(), many=True).data
        
        return data

class ThematicCategorizationTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = ThematicCategorizationType
        fields = ('id', 'name', 'code', 'created', 'updated')

class ClassifierSerializer(serializers.ModelSerializer):

    class Meta:
        model = Classifier
        fields = ('id', 'name', 'code', 'created', 'updated')

class IndicatorSerializer(serializers.ModelSerializer):

    class Meta:
        model = IndicatorAdaptation
        fields = ('id', 'name', 'description', 'unit', 'methodological_detail', 'reporting_periodicity', 'available_time_start_date', 'available_time_end_date', 'geographic_coverage', 'other_geographic_coverage', 'adaptation_action',
         'disaggregation', 'limitation', 'additional_information', 'comments', 'information_source', 'type_of_data', 'other_type_of_data', 'classifier', 'other_classifier', 'contact', 'additional_information_file', 'methodological_detail_file', 'created', 'updated')
    
    def _get_url(self, obj):
        
        return reverse('get_put_indicator_file_adaptation_action', kwargs={'adaptation_action_id':  obj.adaptation_action.id , 'file_id': obj.id})

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['information_source'] = InformationSourceSerializer(instance.information_source).data
        data['type_of_data'] = ThematicCategorizationTypeSerializer(instance.type_of_data).data
        data['classifier'] = ClassifierSerializer(instance.classifier.all(), many=True).data
        data['contact'] = ContactSerializer(instance.contact).data
        data['methodological_detail_file'] = self._get_url(instance)
        data['additional_information_file'] = self._get_url(instance)

        return data

#Serializer section 5-6


class ProgressLogSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProgressLog
        fields = ('id', 'action_status', 'progress_monitoring', 'created', 'updated')

class IndicatorSourceSerializer(serializers.ModelSerializer):

    class Meta:
        model = IndicatorSource
        fields = ('id', 'code', 'name', 'created', 'updated')

class IndicatorMonitoringSerializer(serializers.ModelSerializer):

    class Meta:
        model = IndicatorMonitoring
        fields = ('id', 'start_date', 'end_date', 'update_date', 'data_to_update', 'indicator_source', 'indicator', 'data_to_update_file',
                  'other_indicator_source', 'support_information', 'adaptation_action')

    def _get_url(self, obj):
        
        return reverse('get_put_monitoring_indicator_file_adaptation_action', kwargs={'adaptation_action_id':  obj.adaptation_action.id , 'file_id': obj.id})

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['indicator_source'] = IndicatorSourceSerializer(instance.indicator_source.all(), many=True).data
        data['indicator'] = IndicatorSerializer(instance.indicator).data
        data['data_to_update_file'] = self._get_url(instance)

        return data

class GeneralReportSerializer(serializers.ModelSerializer):

    class Meta:
        model = GeneralReport
        fields = ('id', 'description', 'created', 'updated')

class TemporalityImpactSerializer(serializers.ModelSerializer):

    class Meta:
        model = TemporalityImpact
        fields = ('id', 'code', 'name', 'created', 'updated')

class ActionImpactSerializer(serializers.ModelSerializer):

    class Meta:
        model = ActionImpact
        fields = ('id', 'gender_equality', 'gender_equality_description', 'unwanted_action', 'unwanted_action_description', 'general_impact', 'temporality_impact', 'ods', 'data_to_update_file_action_impact')
    
    def _get_url(self, obj, file_name):
        
        return reverse('get_file_to_adaptation_action', kwargs={'model_id': obj.id, 'file_name': file_name})

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['general_impact'] = GeneralImpactSerializer(instance.general_impact).data
        data['temporality_impact'] = TemporalityImpactSerializer(instance.temporality_impact.all(), many=True).data
        data['ods'] = ODSSerializer(instance.ods.all(), many=True).data
        data['data_to_update_file_action_impact'] = self._get_url(instance, 'data_to_update_file_action_impact')

        return data
    
    
class ChangeLogSerializer(serializers.ModelSerializer):

    class Meta:
        model = ChangeLog
        fields = ('id', 'date', 'adaptation_action', 'previous_status', 'current_status', 'user')
        
        
class AdaptationActionSerializer(serializers.ModelSerializer):

    class Meta:
        model = AdaptationAction
        fields = ('id', 'code', 'fsm_state', 'report_organization', 'address', 'adaptation_action_information','activity', 'instrument', 'climate_threat', 'implementation', 'finance', 'progress_log', 'general_report', 'action_impact', 'review_count', 'comments','user', 'created', 'updated')

    def _get_fsm_state_info(self, instance):
        
        data = {
            'state': instance.fsm_state,
            'label':  _(AA_FSM_STATE.get(instance.fsm_state), 'label'),
        }
        return data
    
    def _next_action(self, instance):
        
        transitions = instance.get_available_fsm_state_transitions()
        result = [
                    {
                        'state':transition.target, 
                        'label': _(AA_FSM_STATE.get(instance.fsm_state), 'label'),
                        'required_comments': True
                    } for transition in transitions
                ]
        return result


    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['fsm_state'] = self._get_fsm_state_info(instance)
        data['next_state'] = self._next_action(instance)
        data['report_organization'] = ReportOrganizationSerializer(instance.report_organization).data
        data['address'] = AddressSerializer(instance.address).data
        data['adaptation_action_information'] = AdaptationActionInformationSerializer(instance.adaptation_action_information).data
        data['activity'] = ActivitySerializer(instance.activity.all(), many=True).data
        data['instrument'] = InstrumentSerializer(instance.instrument).data
        data['climate_threat'] = ClimateThreatSerializer(instance.climate_threat).data
        data['implementation'] = ImplementationSerializer(instance.implementation).data
        data['finance'] = FinanceSerializer(instance.finance).data
        data['indicator_list'] = IndicatorSerializer(instance.indicator.all(), many=True).data
        data['progress_log'] = ProgressLogSerializer(instance.progress_log).data
        data['indicator_monitoring_list'] = IndicatorMonitoringSerializer(instance.indicator_monitoring.all(), many=True).data
        data['general_report'] = GeneralReportSerializer(instance.general_report).data
        data['action_impact'] = ActionImpactSerializer(instance.action_impact).data
        data['change_log'] = ChangeLogSerializer(instance.change_log.all()[:10], many=True).data
        data['comments'] = CommentSerializer(instance.comments.filter(
            fsm_state=instance.fsm_state, review_number=instance.review_count
        ), many=True).data
        
        return data

