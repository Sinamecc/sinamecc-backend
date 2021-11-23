
from django.db.models import fields
from rest_framework import serializers

from adaptation_action.models import ODS, AdaptationAction, AdaptationActionInformation, AdaptationActionType, AdaptationAxis, AdaptationGuideline, ClimateThreat, Implementation, Instrument, NDCArea, NDCContribution, ReportOrganization, ReportOrganizationType, Topics, SubTopics, Activity, TypeClimatedThreat, AdaptationGuidelineMeta, AdaptationAxisGuideline
from general.serializers import AddressSerializer

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
        model = AdaptationAxisGuideline
        fields = ('id', 'code', 'name', 'adaptation_axis', 'created', 'updated')

class AdaptationGuidelineSerializer(serializers.ModelSerializer):

    class Meta:
        model = AdaptationGuideline
        fields = ('id', 'code', 'name', 'created', 'updated')

class AdaptationGuidelineMetaSerializer(serializers.ModelSerializer):

    class Meta:
        model = AdaptationGuidelineMeta
        fields = ('id', 'code', 'meta', 'adaptation_guideline', 'created', 'updated')

class NDCAreaSerializer(serializers.ModelSerializer):

    class Meta:
        model = NDCArea
        fields = ('id', 'code', 'description', 'other', 'created', 'updated')

class NDCContributionSerializer(serializers.ModelSerializer):

    class Meta:
        model = NDCContribution
        fields = ('id', 'code', 'description', 'other', 'ndc_area', 'created', 'updated')


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

class AdaptationActionSerializer(serializers.ModelSerializer):

    class Meta:
        model = AdaptationAction
        fields = ('id', 'report_organization', 'address', 'adaptation_action_information','activity', 'instrument', 'climate_threat', 'implementation', 'created', 'updated')

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['report_organization'] = ReportOrganizationSerializer(instance.report_organization).data
        data['address'] = AddressSerializer(instance.address).data
        data['adaptation_action_information'] = AdaptationActionInformationSerializer(instance.adaptation_action_information).data
        data['activity'] = ActivitySerializer(instance.activity).data
        data['instrument'] = InstrumentSerializer(instance.instrument).data
        data['climate_threat'] = ClimateThreatSerializer(instance.climate_threat).data
        data['implementation'] = ImplementationSerializer(instance.implementation).data
        return data

