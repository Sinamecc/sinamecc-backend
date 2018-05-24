from rest_framework import serializers
from mitigation_action.models import RegistrationType, Institution, Contact, Status, ProgressIndicator, FinanceSourceType, Finance, IngeiCompliance, GeographicScale, Location, Mitigation

class RegistrationTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegistrationType
        fields = ('type')

class InstitutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Institution
        fields = ('name')

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ('full_name', 'job_title', 'email', 'phone')

class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = ('status')

class ProgressIndicatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProgressIndicator
        fields = ('name', 'type', 'unit', 'start_date')

class FinanceSourceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinanceSourceType
        fields = ('name')

class FinanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Finance
        fields = ('finance_source_type', 'source')

class IngeiComplianceSerializer(serializers.ModelSerializer):
    class Meta:
        model = IngeiCompliance
        fields = ('name')

class GeographicScaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeographicScale
        fields = ('name')

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ('geographical_site', 'is_gis_annexed')

class MitigationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mitigation
        fields = (
            'id',
            'strategy_name',
            'name',
            'purpose',
            'quantitative_purpose',
            'start_date',
            'end_date',
            'gas_inventory',
            'emissions_source',
            'carbon_sinks',
            'impact_plan',
            'impact',
            'bibliographic_sources',
            'is_international',
            'international_participation',
            'sustainability',
            'question_ucc',
            'question_ovv',
            'user',
            'registration_type',
            'institution',
            'contact',
            'status',
            'progress_indicator',
            'finance',
            'geographic_scale',
            'location',
            'review_count',
            'review_status',
            'comments',
            'created',
            'updated'
        )
