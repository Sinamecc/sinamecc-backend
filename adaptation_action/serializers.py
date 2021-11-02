
from django.db import models
from django.db.models import fields
from rest_framework import serializers

from adaptation_action.models import ODS, AdaptationAction, AdaptationActionInformation, AdaptationActionType, AdaptationAxis, AdaptationGuideline, ClimateThreat, FinanceAdaptation, FinanceSourceType, FinanceStatus, Implementation, IndicatorAdaptation, InformationSource, InformationSourceType, Instrument, Mideplan, NDCArea, NDCContribution, ReportOrganization, ReportOrganizationType, ThematicCategorizationType, Topics, SubTopics, Activity, TypeClimatedThreat, Classifier


class ReportOrganizationTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = ReportOrganizationType
        fields = ('id', 'code', 'entity_type', 'created', 'updated')

class ReportOrganizationSerializer(serializers.ModelSerializer):

    class Meta:
        model = ReportOrganization
        fields = ('id', 'responsible_entity', 'legal_identification', 'elaboration_date', 'entity_address', 'report_organization_type','contact', 'created', 'updated')

class AdaptationActionTypeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = AdaptationActionType
        fields = ('id', 'name', 'created', 'updated')

class ODSSerializer(serializers.ModelSerializer):

    class Meta:
        model = ODS
        fields = ('id', 'code', 'name', 'created', 'updated')

class AdaptationActionInformationSerializer(serializers.ModelSerializer):

    class Meta:
        model = AdaptationActionInformation
        fields = ('id', 'name', 'objective', 'description', 'meta', 'adaptation_action_type', 'ods', 'created', 'updated')

class TopicsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Topics
        fields = ('id', 'code', 'name', 'created', 'updated')

class SubTopicsSerializer(serializers.ModelSerializer):

    class Meta:
        model = SubTopics
        fields = ('id', 'code', 'name', 'topic', 'created', 'updated')

class AdaptationAxisSerializer(serializers.ModelSerializer):

    class Meta:
        model = AdaptationAxis
        fields = ('id', 'code', 'description', 'created', 'updated')

class AdaptationAxisGuidelineSerializer(serializers.ModelSerializer):

    class Meta:
        model = AdaptationAxis
        fields = ('id', 'code', 'name', 'adaptation_axis', 'created', 'updated')

class AdaptatitionGuidelineSerializer(serializers.ModelSerializer):

    class Meta:
        model = AdaptationGuideline
        fields = ('id', 'code', 'name', 'created', 'updated')

class AdaptatitionGuidelineMetaSerializer(serializers.ModelSerializer):

    class Meta:
        model = AdaptationGuideline
        fields = ('id', 'code', 'meta', 'adaptation_guideline', 'created', 'updated')

class NDCAreaSerializer(serializers.ModelSerializer):

    class Meta:
        model = NDCArea
        fields = ('id', 'code', 'description', 'created', 'updated')

class NDCContributionSerializer(serializers.ModelSerializer):

    class Meta:
        model = NDCContribution
        fields = ('id', 'code', 'description', 'ndc_area', 'created', 'updated')


class ActivitySerializer(serializers.ModelSerializer):

    class Meta:
        model = Activity
        fields = ('id', 'code', 'description', 'sub_topic', 'adaptation_guideline_meta', 'ndc_contribution', 'adaptation_axis_guideline', 'created', 'updated')

class InstrumentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Instrument
        fields = ('id', 'name', 'description', 'created', 'updated')

class TypeClimatedThreatSerializer(serializers.ModelSerializer):

    class Meta:
        model = TypeClimatedThreat
        fields = ('id', 'code', 'name', 'created', 'updated')

class ClimateThreatSerializer(serializers.ModelSerializer):

    class Meta:
        model = ClimateThreat
        fields = ('id', 'type_climated_threat', 'created', 'updated')

class ImplementationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Implementation
        fields = ('id', 'start_date', 'end_date', 'duration', 'responsible_entity', 'other_entity', 'action_code', 'created', 'updated')

#Serializer section 3-4

class FinanceStatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = FinanceStatus
        fields = ('id', 'name', 'code', 'created', 'updated')

class FinanceSourceTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = FinanceSourceType
        fields = ('id', 'name', 'code', 'created', 'updated')

class MideplanSerializer(serializers.ModelSerializer):

    class Meta:
        model = Mideplan
        fields = ('id', 'registry', 'name', 'entity', 'created', 'updated')

class FinanceSerializer(serializers.ModelSerializer):

    class Meta:
        model = FinanceAdaptation
        fields = ('id', 'administration', 'budget', 'status', 'source', 'finance_instrument', 'mideplan', 'created', 'updated')

class InformationSourceTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = InformationSourceType
        fields = ('id', 'name', 'code', 'created', 'updated')

class InformationSourceSerializer(serializers.ModelSerializer):

    class Meta:
        model = InformationSource
        fields = ('id', 'responsible_institution', 'type', 'other_type', 'statistical_operation', 'created', 'updated')

class ThematicCategorizationTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = ThematicCategorizationType
        fields = ('id', 'name', 'code', 'created', 'updated')

class Classifier(serializers.ModelSerializer):

    class Meta:
        model = Classifier
        fields = ('id', 'name', 'code', 'created', 'updated')

class IndicatorSerializer(serializers.ModelSerializer):

    class Meta:
        model = IndicatorAdaptation
        fields = ('id', 'name', 'description', 'unit', 'methodological_detail', 'reporting_periodicity', 'available_time_start_date', 'geographic_coverage', 'other_geographic_coverage',
         'disaggregation', 'limitation', 'additional_information', 'comments', 'information_source', 'type_of_data', 'other_type_of_data', 'classifier', 'other_classifier', 'contact', 'created', 'updated')


class AdaptationActionSerializer(serializers.ModelSerializer):

    class Meta:
        model = AdaptationAction
        fields = ('id', 'report_organization', 'address', 'adaptation_action_information','activity', 'instrument', 'climate_threat', 'implementation', 'created', 'updated')

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['report_organization'] = ReportOrganizationSerializer(instance.report_organization).data
        #data['address'] = 
        data['adaptation_action_information'] = AdaptationActionInformationSerializer(instance.adaptation_action_information).data
        data['activity'] = ActivitySerializer(instance.activity).data
        data['instrument'] = InstrumentSerializer(instance.instrument).data
        data['climate_threat'] = ClimateThreatSerializer(instance.climate_threat).data
        data['implementation'] = ImplementationSerializer(instance.implementation).data
        return data

