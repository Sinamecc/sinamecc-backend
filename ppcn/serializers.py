from rest_framework import serializers
from ppcn.models import Organization, GeographicLevel, Contact, RequiredLevel, RecognitionType, PPCN, PPCNFile

class GeographicLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeographicLevel
        fields = ('level_es', 'level_en')

class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ('id', 'name', 'representative_name','phone_organization', 'postal_code', 'fax', 'address', 'ciiu', 'contact')


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

class PPCNSerializer(serializers.ModelSerializer):
    class Meta:
        model = PPCN
        fields = ('id','organization', 'geographicLevel', 'requiredLevel', 'sector','subsector', 'recognitionType', 'base_year', 'created', 'updated')

class PPCNFileSeriaizer (serializers.ModelSerializer):
    class Meta:
        model = PPCNFile
        fields = ('id', 'user', 'file', 'created', 'updated', 'ppcn_form')