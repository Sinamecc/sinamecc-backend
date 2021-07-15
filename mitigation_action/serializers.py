from general import models
from django.utils.translation import override
from rest_framework import serializers
from mitigation_action.models import Finance, MitigationAction, Contact, Status, FinanceSourceType, GeographicScale,\
    InitiativeType, FinanceStatus, InitiativeGoal, Initiative, MitigationActionStatus, GeographicLocation, GHGInformation, \
        ImpactDocumentation, QAQCReductionEstimateQuestion, Indicator, MonitoringInformation, MonitoringIndicator, MonitoringReportingIndicator


##
## Auxiliar Class Serializer
##
class GenericListSerializer(serializers.ListSerializer):
    def update(self, instance, validated_data):
        # Maps for id->instance and id->data item.
        record_mapping = {record.id: record for record in instance}
        data_mapping = {}
        new_record_list = []

        for item in validated_data:
            if item.get('id', False):
                data_mapping[item.get('id')] = item
            else:
                new_record_list.append(item)

        # Perform creations and updates.
        ret = []

        for record_id, data in data_mapping.items():
            record = record_mapping.get(record_id, None)
            if record is None:
                ret.append(self.child.create(data))
            else:
                ret.append(self.child.update(record, data))

        for data in new_record_list:
            ret.append(self.child.create(data))


        # Perform deletions.
        for record_id, record in record_mapping.items():
            if record_id not in data_mapping:
                record.delete()

        return ret


##
## Start Catalogs Serializers
##
class InitiativeTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = InitiativeType
        fields = ('id', 'code', 'name', 'type')


class GeographicScaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeographicScale
        fields = ('id', 'code', 'name')


class FinanceSourceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinanceSourceType
        fields = ('id', 'code','name')


class FinanceStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinanceStatus
        fields = ('id', 'code', 'name')


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = ('id', 'code', 'status')


##
## Finish Catalogs Serializers
##


##
## Start Model Serializers
##

class QAQCReductionEstimateQuestionSerializer(serializers.ModelSerializer):

    id = serializers.IntegerField()
    class Meta:
        model = QAQCReductionEstimateQuestion
        fields = ('id', 'code', 'question', 'check', 'detail', 'impact_documentation')
        list_serializer_class = GenericListSerializer


class MonitoringIndicatorSerializer(serializers.ModelSerializer):

    id = serializers.IntegerField()
    class Meta:
        model = MonitoringIndicator
        fields = ('id', 'initial_date_report_period', 'final_date_report_period', 'data_updated_date', 'updated_data', 'progress_report', 'indicator', 'monitoring_reporting_indicator')
        list_serializer_class = GenericListSerializer


class IndicatorSerializer(serializers.ModelSerializer):

    id = serializers.IntegerField()
    class Meta:
        model = Indicator
        fields = ('id', 'name', 'description', 'type', 'unit' , 'methodological_detail', 'reporting_periodicity', 'data_generating_institution',\
                    'reporting_institution', 'measurement_start_date', 'additional_information', 'monitoring_information')
        list_serializer_class = GenericListSerializer


class MonitoringInformationSerializer(serializers.ModelSerializer):

    class Meta:
        model = MonitoringInformation
        fields = ('id', 'code')

    def to_representation(self, instance):

        data = super().to_representation(instance)
        data['indicator'] = IndicatorSerializer(instance.indicator.all(), many=True).data

        return data


class MonitoringReportingIndicatorSerializer(serializers.ModelSerializer):

    class Meta:
        model = MonitoringReportingIndicator
        fields = ('id', 'progress_in_monitoring')

    def to_representation(self, instance):

        data = super().to_representation(instance)
        data['monitoring_indicator'] = MonitoringIndicatorSerializer(instance.monitoring_indicator.all(), many=True).data

        return data


class ImpactDocumentationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImpactDocumentation
        fields = ('id', 'estimate_reduction_co2', 'period_potential_reduction', 'base_line_definition', 'calculation_methodology', 
                        'estimate_calculation_documentation', 'mitigation_action_in_inventory', 'carbon_international_commerce', 
                        'methodologies_to_use')
        
    def to_representation(self, instance):

        data = super().to_representation(instance)
        data['question'] = QAQCReductionEstimateQuestionSerializer(instance.question.all(), many=True).data

        return data


class GHGInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = GHGInformation
        fields = ('id', 'impact_emission', 'graphic_description') 


class FinanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Finance
        fields = ('id', 'status', 'administration', 'source', 'source_description', 'reference_year', 'budget',
                    'currency', 'mideplan_registered', 'mideplan_project', 'executing_entity')


class InitiativeGoalSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    class Meta:
        model = InitiativeGoal
        fields = ('id', 'goal', 'initiative')
        list_serializer_class = GenericListSerializer
        

class InitiativeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Initiative
        fields = ('id', 'name', 'objective', 'description', 'description_file', 'initiative_type')

    def _get_description_file_url(self, instance):

        if instance.description_file:

            return 'fake/url/{0}'.format(instance.description_file.name)
        
        return None


    def to_representation(self, instance):

        data = super().to_representation(instance)
        data['initiative_type'] = InitiativeTypeSerializer(instance.initiative_type).data
        data['description_file'] = self._get_description_file_url(instance)
        data['goal'] = InitiativeGoalSerializer(instance.goal.all(), many=True).data

        return data


class MitigationActionStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = MitigationActionStatus
        fields = ('id', 'status', 'start_date', 'end_date', 'other_end_date', 'institution', 'other_institution')

    def to_representation(self, instance):

        data = super().to_representation(instance)
        data['status'] = StatusSerializer(instance.status).data
        
        return data


class GeographicLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeographicLocation
        fields = ('id', 'geographic_scale', 'location')

    def to_representation(self, instance):

        data = super().to_representation(instance)
        data['geographic_scale'] = GeographicScaleSerializer(instance.geographic_scale).data

        return data


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ('id', 'institution', 'full_name', 'job_title', 'email', 'phone', 'user', 'created', 'updated')


class MitigationActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = MitigationAction
        fields = ('id', 'fsm_state','contact', 'initiative', 'status_information', 'geographic_location', 'finance', 
                    'ghg_information', 'impact_documentation', 'monitoring_information', 'monitoring_reporting_indicator', 
                    'user', 'created', 'updated')
    
    def to_representation(self, instance):

        data = super().to_representation(instance)
        data['contact'] = ContactSerializer(instance.contact).data
        data['initiative'] = InitiativeSerializer(instance.initiative).data
        data['status_information'] = MitigationActionStatusSerializer(instance.status_information).data
        data['geographic_location'] = GeographicLocationSerializer(instance.geographic_location).data
        data['finance'] = FinanceSerializer(instance.finance).data
        data['ghg_information'] = GHGInformationSerializer(instance.ghg_information).data
        data['impact_documentation'] = ImpactDocumentationSerializer(instance.impact_documentation).data
        data['monitoring_information'] = MonitoringInformationSerializer(instance.monitoring_information).data
        data['monitoring_reporting_indicator'] = MonitoringReportingIndicatorSerializer(instance.monitoring_reporting_indicator).data

        return data




