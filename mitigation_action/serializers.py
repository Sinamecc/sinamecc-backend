from rest_framework import serializers
from mitigation_action.models import ActionAreas, ActionGoals, Finance, MitigationAction, Contact, Status, FinanceSourceType, GeographicScale,\
    InitiativeType, FinanceStatus, InitiativeGoal, Initiative, MitigationActionStatus, GeographicLocation, GHGInformation, \
    ImpactDocumentation, QAQCReductionEstimateQuestion, Indicator, MonitoringInformation, MonitoringIndicator, MonitoringReportingIndicator, \
    ActionAreas, ActionGoals, DescarbonizationAxis, TransformationalVisions, Topics, SubTopics, Activity,  ImpactCategory, Categorization, SustainableDevelopmentGoals, \
    GHGImpactSector, CarbonDeposit, Standard, InformationSource, InformationSourceType, ThematicCategorizationType, Classifier, IndicatorChangeLog, \
    FinanceInformation

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
class SustainableDevelopmentGoalsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SustainableDevelopmentGoals
        fields = ('id', 'code', 'description')


class GHGImpactSectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = GHGImpactSector
        fields = ('id', 'code', 'name')


class CarbonDepositSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarbonDeposit
        fields = ('id', 'code', 'name')


class StandardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Standard
        fields = ('id', 'code', 'name')


class ActionAreasSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActionAreas
        fields = ('id', 'name', 'code')


class ActionGoalsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActionGoals
        fields = ('id', 'goal', 'code', 'area')


class DescarbonizationAxisSerializer(serializers.ModelSerializer):
    class Meta:
        model = DescarbonizationAxis
        fields = ('id', 'description', 'code')


class TransformationalVisionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransformationalVisions
        fields = ('id', 'description', 'code', 'axis')


class TopicsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topics
        fields = ('id', 'name', 'code')

class SubTopicsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubTopics
        fields = ('id', 'name', 'code', 'topic')


class ImpactCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ImpactCategory
        fields = ('id', 'code', 'name')


class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = ('id', 'description', 'code', 'sub_topic')


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


class InformationSourceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = InformationSourceType
        fields = ('id', 'code', 'name')


class ThematicCategorizationTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ThematicCategorizationType
        fields = ('id', 'code', 'name')

class ClassifierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Classifier
        fields = ('id', 'code', 'name')
        
##
## Finish Catalogs Serializers
##


##
## Start Model Serializers
##
## Edit this serializers
class CategorizationSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Categorization
        fields = ('id', 'action_goal', 'transformational_vision', 'sub_topics', 'activities', 'impact_categories', 'is_part_to_another_mitigation_action', 'relation_description')
    
    def to_representation(self, instance):
        
        data = super().to_representation(instance)
        data['action_goal'] = ActionGoalsSerializer(instance.action_goal.all(), many=True).data
        data['transformational_vision'] = TransformationalVisionsSerializer(instance.transformational_vision.all(), many=True).data
        data['sub_topics'] = SubTopicsSerializer(instance.sub_topics.all(), many=True).data
        data['activities'] = ActivitySerializer(instance.activities.all(), many=True).data
        data['impact_categories'] = ImpactCategorySerializer(instance.impact_categories.all(), many=True).data

        return data


class QAQCReductionEstimateQuestionSerializer(serializers.ModelSerializer):

    id = serializers.IntegerField()
    class Meta:
        model = QAQCReductionEstimateQuestion
        fields = ('id', 'code', 'question', 'check', 'detail', 'impact_documentation')
        list_serializer_class = GenericListSerializer


class MonitoringIndicatorSerializer(serializers.ModelSerializer):

    class Meta:
        model = MonitoringIndicator
        fields = ('id', 'initial_date_report_period', 'final_date_report_period', 'data_updated_date', 'updated_data', 'progress_report', 'indicator', 'monitoring_reporting_indicator')
        


class IndicatorChangeLogSerializer(serializers.ModelSerializer):

    class Meta:
        model = IndicatorChangeLog
        fields = ('id', 'indicator', 'update_date', 'changes', 'changes_description', 'author')



class IndicatorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Indicator

        fields = ('id', 'name', 'description', 'unit', 'methodological_detail', 'methodological_detail_file', 'reporting_periodicity', 'available_time_start_date', 'available_time_end_date', 
                'geographic_coverage', 'other_geographic_coverage', 'disaggregation', 'limitation', 'additional_information', 'additional_information_file', 'comments',
                'information_source', 'type_of_data', 'other_type_of_data', 'classifier', 'other_classifier', 'contact', 'monitoring_information')
    

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['contact'] = ContactSerializer(instance.contact).data
        data['information_source'] = InformationSourceSerializer(instance.information_source).data
        data['change_log'] = IndicatorChangeLogSerializer(instance.indicator_change_log.all(), many=True).data
        ## push the indicator_id to the indicator_change_log
        return data


class InformationSourceSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = InformationSource
        fields = ('id', 'responsible_institution', 'type', 'other_type', 'statistical_operation')


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
        fields = ('id', 'estimate_reduction_co2', 'period_potential_reduction', 'base_line_definition', 'carbon_deposit','calculation_methodology', 
                    'estimate_calculation_documentation', 'estimate_calculation_documentation_file', 'mitigation_action_in_inventory', 'standard', 
                    'other_standard', 'carbon_international_commerce', 'methodologies_to_use')
    

    def _get_estimate_calculation_documentation_file_url(self, instance):

        if instance.estimate_calculation_documentation_file:

            return 'fake/url/{0}'.format(instance.estimate_calculation_documentation_file.name)
        
        return None

    def to_representation(self, instance):

        data = super().to_representation(instance)
        data['question'] = QAQCReductionEstimateQuestionSerializer(instance.question.all(), many=True).data
        data['carbon_deposit'] = CarbonDepositSerializer(instance.carbon_deposit).data
        data['standard'] =  StandardSerializer(instance.standard).data
        data['estimate_calculation_documentation_file'] = self._get_estimate_calculation_documentation_file_url(instance)

        return data


class GHGInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = GHGInformation
        fields = ('id', 'impact_emission', 'graphic_description', 'graphic_description_file', 'impact_sector', 'goals')
    

    def _get_graphic_description_file_url(self, instance):

        if instance.graphic_description_file:

            return 'fake/url/{0}'.format(instance.graphic_description_file.name)
        
        return None


    def to_representation(self, instance):
        
        data = super().to_representation(instance)
        data['impact_sector'] = GHGImpactSectorSerializer(instance.impact_sector.all(), many=True).data
        data['goals'] = SustainableDevelopmentGoalsSerializer(instance.goals.all(), many=True).data
        data['graphic_description_file'] = self._get_graphic_description_file_url(instance)

        return data


class FinanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Finance
        fields = ('id', 'status', 'administration', 'source', 'reference_year',
                  'mideplan_registered', 'mideplan_project', 'executing_entity')
        
        
    def to_representation(self, instance):
        
        data = super().to_representation(instance)
        data['finance_information'] = FinanceInformationSerializer(instance.finance_information.all(), many=True).data
        
        return data


class FinanceInformationSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    class Meta:
        model = FinanceInformation
        fields = ('id', 'source_description', 'budget', 'currency', 'finance')
        list_serializer_class = GenericListSerializer
        

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
        fields = ('id', 'geographic_scale', 'location', 'location_file')

    
    def _get_location_file_url(self, instance):

        if instance.location_file:

            return 'fake/url/{0}'.format(instance.location_file.name)
        
        return None


    def to_representation(self, instance):

        data = super().to_representation(instance)
        data['geographic_scale'] = GeographicScaleSerializer(instance.geographic_scale).data
        data['location_file'] = self._get_location_file_url(instance)

        return data


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ('id', 'institution', 'full_name', 'job_title', 'email', 'phone', 'user', 'created', 'updated')

    
class MitigationActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = MitigationAction
        fields = ('id', 'code', 'fsm_state','contact', 'initiative', 'status_information', 'geographic_location', 'categorization','finance', 
                    'ghg_information', 'impact_documentation', 'monitoring_information', 'monitoring_reporting_indicator', 
                    'user', 'created', 'updated')
        # only read code kwargs
        extra_kwargs = {
            'code': {'read_only': True}
        }
          
    
    def to_representation(self, instance):

        data = super().to_representation(instance)
        data['contact'] = ContactSerializer(instance.contact).data
        data['initiative'] = InitiativeSerializer(instance.initiative).data
        data['status_information'] = MitigationActionStatusSerializer(instance.status_information).data
        data['geographic_location'] = GeographicLocationSerializer(instance.geographic_location).data
        data['categorization'] = CategorizationSerializer(instance.categorization).data
        data['finance'] = FinanceSerializer(instance.finance).data
        data['ghg_information'] = GHGInformationSerializer(instance.ghg_information).data
        data['impact_documentation'] = ImpactDocumentationSerializer(instance.impact_documentation).data
        data['monitoring_information'] = MonitoringInformationSerializer(instance.monitoring_information).data
        data['monitoring_reporting_indicator'] = MonitoringReportingIndicatorSerializer(instance.monitoring_reporting_indicator).data

        return data



