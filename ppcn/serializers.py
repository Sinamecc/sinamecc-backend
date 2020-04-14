from rest_framework import serializers
from ppcn.models import Organization, GeographicLevel, Contact, RequiredLevel, RecognitionType, GeiOrganization, PPCN, PPCNFile, ChangeLog, GeiActivityType

class GeographicLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeographicLevel
        fields = ('level_es', 'level_en')

class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ('id', 'name', 'legal_identification','representative_name','phone_organization', 'postal_code', 'fax', 'address', 'ciiu', 'contact')


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ('id','full_name', 'job_title', 'email', 'phone')

class RequiredLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequiredLevel
        fields = ('level_type_es', 'level_type_en')

class RecognitionTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecognitionType
        fields = ('recognition_type_es', 'recognition_type_en')

class GeiOrganizationSerializer(serializers.ModelSerializer):

    class Meta:
        model =  GeiOrganization
        fields = ('id', 'ovv', 'emission_ovv_date', 'report_year', 'base_year')

class GeiActivityTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model =  GeiActivityType
        fields = ('id', 'activity_type', 'sub_sector', 'sector')

class ChangeLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChangeLog
        fields = ('ppcn', 'previous_status', 'current_status', 'user')

class PPCNSerializer(serializers.ModelSerializer):
    class Meta:
        model = PPCN
        fields = ('id','user','organization', 'gei_organization','geographic_level', 'required_level', 'recognition_type', 'fsm_state' , 'review_count', 'created', 'updated')

class PPCNFileSeriaizer (serializers.ModelSerializer):
    class Meta:
        model = PPCNFile
        fields = ('id', 'user', 'file', 'created', 'updated', 'ppcn_form')