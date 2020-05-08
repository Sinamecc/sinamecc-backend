from rest_framework import serializers
from ppcn.models import  Organization, GeographicLevel, Contact, RequiredLevel, RecognitionType, GeiOrganization,\
                            PPCN, PPCNFile, ChangeLog, GeiActivityType, CIIUCode, Sector, SubSector, Reduction, \
                            OrganizationClassification, CarbonOffset, BiogenicEmission, GasReport, GasScope, QuantifiedGas

class GeographicLevelSerializer(serializers.ModelSerializer):

    level = serializers.SerializerMethodField('language')
    class Meta:
        model = GeographicLevel
        fields = ('id', 'level_es', 'level_en', 'level')
        extra_kwargs = {
            'level_es': {'write_only': True},
            'level_en': {'write_only': True},
            'level': {'read_only': True}
        }

    def language(self, obj):
        return  obj.level_en if self.context.get('language', 'en') == 'en' else obj.level_es


class RequiredLevelSerializer(serializers.ModelSerializer):

    level_type = serializers.SerializerMethodField('language')
    class Meta:
        model = RequiredLevel
        fields = ('id', 'level_type_es', 'level_type_en', 'level_type')
        extra_kwargs = {
            'level_type_es': {'write_only': True},
            'level_type_en': {'write_only': True},
            'level_type': {'read_only': True}
        }
    
    def language(self, obj):
        return  obj.level_type_en if self.context.get('language', 'en') == 'en' else obj.level_type_es


class RecognitionTypeSerializer(serializers.ModelSerializer):

    recognition_type = serializers.SerializerMethodField('language')
    class Meta:
        model = RecognitionType
        fields = ('id','recognition_type_es', 'recognition_type_en', 'recognition_type')
        extra_kwargs = {
            'recognition_type_es': {'write_only': True},
            'recognition_type_en': {'write_only': True},
            'recognition_type': {'read_only': True}
        }

    def language(self, obj):
        return  obj.recognition_type_en if self.context.get('language', 'en') == 'en' else obj.recognition_type_es

class SectorSerializer(serializers.ModelSerializer):

    name = serializers.SerializerMethodField('language')
    class Meta:
        model = Sector
        fields = ('id','name_es', 'name_en', 'name')
        extra_kwargs = {
            'name_es': {'write_only': True},
            'name_en': {'write_only': True},
            'name': {'read_only': True}
        }

    def language(self, obj):
        return  obj.name_en if self.context.get('language', 'en') == 'en' else obj.name_es

class SubSectorSerializer(serializers.ModelSerializer):

    name = serializers.SerializerMethodField('language')
    class Meta:
        model = SubSector
        fields = ('id','name_es', 'name_en', 'name', 'sector')
        extra_kwargs = {
            'name_es': {'write_only': True},
            'name_en': {'write_only': True},
            'name': {'read_only': True}
        }

    def language(self, obj):
        return  obj.name_en if self.context.get('language', 'en') == 'en' else obj.name_es

class ReductionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Reduction
        fields = ('id', 'project', 'activity', 'detail_reduction', 'emission', 'total_emission', 'investment', 
                    'investment_currency', 'total_investment', 'total_investment_currency')

class CarbonOffsetSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarbonOffset
        fields = ('id', 'offset_scheme', 'project_location', 'certificate_identification', 'total_carbon_offset', 
                    'offset_cost', 'offset_cost_currency', 'period', 'total_offset_cost', 'total_offset_cost_currency')

class OrganizationClassificationSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrganizationClassification
        fields = ('id', 'emission_quantity', 'buildings_number', 'data_inventory_quantity', 'required_level', 'recognition_type', 'reduction', 'carbon_offset')


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ('id', 'name', 'legal_identification','representative_name','representative_legal_identification','phone_organization', 'postal_code', 'fax', 'address', 'contact')

class CIIUCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CIIUCode
        fields = ('id', 'organization', 'ciiu_code')

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ('id','full_name', 'job_title', 'email', 'phone')

class BiogenicEmissionSerializer(serializers.ModelSerializer):
    
    class Meta:
        model =  BiogenicEmission
        fields = ('id', 'total', 'scope_1', 'scope_2')


class GasReportSerializer(serializers.ModelSerializer):

    class Meta:
        model = GasReport
        fields = ('id', 'biogenic_emission', 'other_gases', 'cost_ghg_inventory', 'cost_ghg_inventory_currency',
                        'cost_ovv_process', 'cost_ovv_process_currency') 

class GasScopeSerializer(serializers.ModelSerializer):

    class Meta:
        model = GasScope
        fields = ('id', 'name', 'gas_report') 


class QuantifiedGasSerializer(serializers.ModelSerializer):

    class Meta:
        model = QuantifiedGas
        fields = ('id', 'name', 'value', 'gas_scope')


class GeiOrganizationSerializer(serializers.ModelSerializer):

    class Meta:
        model =  GeiOrganization
        fields = ('id', 'ovv', 'emission_ovv_date', 'report_year', 'base_year', 'gas_report')

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
        fields = ('id','user','organization', 'gei_organization','geographic_level', 'organization_classification', 
                    'confidential', 'confidential_fields', 'fsm_state' , 'review_count', 'created', 'updated')

class PPCNFileSeriaizer (serializers.ModelSerializer):
    class Meta:
        model = PPCNFile
        fields = ('id', 'user', 'file', 'created', 'updated', 'ppcn_form')