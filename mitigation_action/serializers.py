from rest_framework import serializers
from mitigation_action.models import RegistrationType, Institution, Contact, Status, ProgressIndicator, Finance, IngeiCompliance, GeographicScale, Location, MitigationAction 

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
        fields = ('type', 'unit', 'start_date')

class FinanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Finance
        fields = ('name', 'source')

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

class MitigationActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = MitigationAction
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
            'user', 
            'registration_type', 
            'institution', 
            'contact', 
            'status', 
            'progress_indicator', 
            'finance', 
            'ingei_compliance', 
            'geographic_scale', 
            'location',
            'created',
            'updated'
        )
