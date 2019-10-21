from rest_framework import serializers
from mitigation_action.models import RegistrationType, Institution, Contact, Status, ProgressIndicator, FinanceSourceType, Finance, IngeiCompliance, \
GeographicScale, Location, ChangeLog,  Mitigation, Initiative, InitiativeType, InitiativeFinance, FinanceStatus

class RegistrationTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegistrationType
        fields = ('id', 'type_es','type_en')

class InstitutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Institution
        fields = ('id', 'name')

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ('id','full_name', 'job_title', 'email', 'phone')

class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = ('id', 'status_es','status_en')

class FinanceStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinanceStatus
        fields = ('id', 'name_es','name_en')

class ProgressIndicatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProgressIndicator
        fields = ('id', 'name', 'type', 'unit', 'start_date')

class FinanceSourceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinanceSourceType
        fields = ('id', 'name_es','name_en')

class FinanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Finance
        fields = ('id', 'status', 'source')
class InitiativeFinanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = InitiativeFinance
        fields = ('id', 'status', 'finance_source_type', 'source')
        
class IngeiComplianceSerializer(serializers.ModelSerializer):
    class Meta:
        model = IngeiCompliance
        fields = ('name_es', 'name_en')

class GeographicScaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeographicScale
        fields = ('id', 'name_es', 'name_en')

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ('id', 'geographical_site', 'is_gis_annexed')

class ChangeLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChangeLog
        fields = ('mitigation_action', 'previous_status', 'current_status', 'user')

class InitiativeTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = InitiativeType
        fields = ('id', 'initiative_type_es', 'initiative_type_en')

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
             'status',
            )

class MitigationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mitigation
        fields = (
            'id',
            'name',
            'purpose',
            'start_date',
            'end_date',
            'gas_inventory',
            'emissions_source',
            'carbon_sinks',
            'impact_plan',
            'impact',
            'calculation_methodology',
            'is_international',
            'international_participation',
            'strategy_name',
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
