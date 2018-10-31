from rest_framework import serializers
from mitigation_action.models import RegistrationType, Institution, Contact, Status, ProgressIndicator, FinanceSourceType, Finance, IngeiCompliance, \
GeographicScale, Location, ChangeLog,  Mitigation, Initiative, InitiativeType, InitiativeFinance

class RegistrationTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegistrationType
        fields = ('type_es','type_en')

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
        fields = ('status_es','status_en')

class ProgressIndicatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProgressIndicator
        fields = ('name', 'type', 'unit', 'start_date')

class FinanceSourceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinanceSourceType
        fields = ('name_es','name_en')

class FinanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Finance
        fields = ('status', 'source')
class InitiativeFinanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = InitiativeFinance
        fields = ('status', 'finance_source_type')
        
class IngeiComplianceSerializer(serializers.ModelSerializer):
    class Meta:
        model = IngeiCompliance
        fields = ('name_es', 'name_en')

class GeographicScaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeographicScale
        fields = ('name_es', 'name_en')

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ('geographical_site', 'is_gis_annexed')

class ChangeLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChangeLog
        fields = ('mitigation_action', 'previous_status', 'current_status', 'user')

class InitiaveSerializer(serializers.ModelSerializer):
     
     class Meta:
         model = Initiative
         fields = (
             'id',
             'name',
             'objective',
             'description',
             'goal',
             'initiative_type',
             'entity_responsible',
             'contact',
             'budget',
             'finance',
             'status'
            )

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
            'initiative',
            'institution',
            'contact',
            'status',
            'progress_indicator',
            'finance',
            'geographic_scale',
            'location',
            'review_count',
            'comments',
            'created',
            'updated'
        )
