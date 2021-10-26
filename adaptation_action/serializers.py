
from django.db.models import fields
from rest_framework import serializers

from adaptation_action.models import AdaptationAction, AdaptationActionInformation, AdaptationActionType, ClimateThreat, Implementation, Instrument, ReportOrganization, Topics, SubTopics, Activity, TypeClimatedThreat

class ReportOrganizationSerializer(serializers.ModelSerializer):

    class Meta:
        model = ReportOrganization
        fields = ('id', 'entity_type', 'responsible_entity', 'legal_identification', 'elaboration_date', 'entity_address', 'contact', 'created', 'updated')

class AdaptationActionTypeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = AdaptationActionType
        fields = ('id', 'name', 'created', 'updated')

class AdaptationActionInformationSerializer(serializers.ModelSerializer):

    class Meta:
        model = AdaptationActionInformation
        fields = ('id', 'name', 'objective', 'description', 'meta','created', 'updated')

class TopicsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Topics
        fields = ('id', 'code', 'name', 'created', 'updated')

class SubTopicsSerializer(serializers.ModelSerializer):

    class Meta:
        model = SubTopics
        fields = ('id', 'code', 'name', 'created', 'updated')

class ActivitySerializer(serializers.ModelSerializer):

    class Meta:
        model = Activity
        fields = ('id', 'code', 'description', 'created', 'updated')

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
        fields = ('id', 'report_organization', 'address', 'activity', 'created', 'updated')

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['report_organization'] = ReportOrganizationSerializer(instance.report_organization).data
        return data

