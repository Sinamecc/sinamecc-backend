from rest_framework import serializers
from mitigation_action.models import ActionAreas, ActionGoals, Finance, MitigationAction, Contact, Status, FinanceSourceType, GeographicScale,\
    InitiativeType, FinanceStatus, InitiativeGoal, Initiative, MitigationActionStatus, GeographicLocation, GHGInformation, \
    ImpactDocumentation, QAQCReductionEstimateQuestion, Indicator, MonitoringInformation, MonitoringIndicator, MonitoringReportingIndicator, \
    ActionAreas, ActionGoals, DescarbonizationAxis, TransformationalVisions, Topics, SubTopics, Activity,  ImpactCategory, Categorization, SustainableDevelopmentGoals, \
    GHGImpactSector, CarbonDeposit, Standard, InformationSource, InformationSourceType, ThematicCategorizationType, Classifier, IndicatorChangeLog, \
    FinanceInformation, ActionAreasSelection, TopicsSelection, ChangeLog, DescarbonizationAxisSelection, Sector, SectorIPCC2006, CategoryIPCC2006, SubCategoryIPCC2006, SectorSelection
from workflow.serializers import CommentSerializer
from general.utils import get_translation_from_database as _
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
    
    description = serializers.SerializerMethodField()
    
    class Meta:
        model = SustainableDevelopmentGoals
        fields = ('id', 'code', 'description')

    def get_description(self, instance):
        return _(instance, 'description')


class GHGImpactSectorSerializer(serializers.ModelSerializer):
    
    name = serializers.SerializerMethodField()
    
    class Meta:
        model = GHGImpactSector
        fields = ('id', 'code', 'name')
        
        
    def get_name(self, instance):
        return _(instance, 'name')


class CarbonDepositSerializer(serializers.ModelSerializer):
    
    name = serializers.SerializerMethodField()
    
    class Meta:
        model = CarbonDeposit
        fields = ('id', 'code', 'name')
        
    
    def get_name(self, instance):
        return _(instance, 'name')


class StandardSerializer(serializers.ModelSerializer):
    
    name = serializers.SerializerMethodField()
    
    class Meta:
        model = Standard
        fields = ('id', 'code', 'name')

    
    def get_name(self, instance):
        return _(instance, 'name')


class ActionAreasSerializer(serializers.ModelSerializer):
    
    name = serializers.SerializerMethodField()
    
    class Meta:
        model = ActionAreas
        fields = ('id', 'name', 'code')

    
    def get_name(self, instance):
        return _(instance, 'name')
    

class ActionGoalsSerializer(serializers.ModelSerializer):
    
    goal = serializers.SerializerMethodField()
    
    class Meta:
        model = ActionGoals
        fields = ('id', 'goal', 'code', 'area')

    
    def get_goal(self, instance):
        return _(instance, 'goal')
    

class DescarbonizationAxisSerializer(serializers.ModelSerializer):
    
    description = serializers.SerializerMethodField()
    
    class Meta:
        model = DescarbonizationAxis
        fields = ('id', 'description', 'code')

    def  get_description(self, instance):
        return _(instance, 'description')
    
    

class TransformationalVisionsSerializer(serializers.ModelSerializer):
    
    description = serializers.SerializerMethodField()
    
    class Meta:
        model = TransformationalVisions
        fields = ('id', 'description', 'code', 'axis')

    
    def get_description(self, instance):
        return _(instance, 'description')
    

class TopicsSerializer(serializers.ModelSerializer):
    
    name = serializers.SerializerMethodField()
    
    class Meta:
        model = Topics
        fields = ('id', 'name', 'code')


    def get_name(self, instance):
        return _(instance, 'name')


class SubTopicsSerializer(serializers.ModelSerializer):
    
    name = serializers.SerializerMethodField()
    
    class Meta:
        model = SubTopics
        fields = ('id', 'name', 'code', 'topic')

    
    def get_name(self, instance):
        return _(instance, 'name')


class ImpactCategorySerializer(serializers.ModelSerializer):
    
    name = serializers.SerializerMethodField()
    
    class Meta:
        model = ImpactCategory
        fields = ('id', 'code', 'name')

    def get_name(self, instance):
        return _(instance, 'name')
    

class ActivitySerializer(serializers.ModelSerializer):
    
    description = serializers.SerializerMethodField()
    
    class Meta:
        model = Activity
        fields = ('id', 'description', 'code', 'sub_topic')

    def  get_description(self, instance):
        return _(instance, 'description')
    

class InitiativeTypeSerializer(serializers.ModelSerializer):
    
    name = serializers.SerializerMethodField()
    
    class Meta:
        model = InitiativeType
        fields = ('id', 'code', 'name', 'type')


    def get_name(self, instance):
        return _(instance, 'name')
    

class GeographicScaleSerializer(serializers.ModelSerializer):
    
    name = serializers.SerializerMethodField()
    
    class Meta:
        model = GeographicScale
        fields = ('id', 'code', 'name')

    
    def get_name(self, instance):
        return _(instance, 'name')
    

class FinanceSourceTypeSerializer(serializers.ModelSerializer):
    
    name = serializers.SerializerMethodField()
    
    class Meta:
        model = FinanceSourceType
        fields = ('id', 'code','name')

    def get_name(self, instance):
        return _(instance, 'name')


class FinanceStatusSerializer(serializers.ModelSerializer):
    
    name = serializers.SerializerMethodField()
    
    class Meta:
        model = FinanceStatus
        fields = ('id', 'code', 'name')


    def get_name(self, instance):
        return _(instance, 'name')
    
    
class StatusSerializer(serializers.ModelSerializer):
    
    status = serializers.SerializerMethodField()
    
    class Meta:
        model = Status
        fields = ('id', 'code', 'status')

    def get_status(self, instance):
        return _(instance, 'status')
    
    

class InformationSourceTypeSerializer(serializers.ModelSerializer):
    
    name = serializers.SerializerMethodField()
    
    class Meta:
        model = InformationSourceType
        fields = ('id', 'code', 'name')
    
    
    def get_name(self, instance):
        return _(instance, 'name')


class ThematicCategorizationTypeSerializer(serializers.ModelSerializer):
    
    name = serializers.SerializerMethodField()
    
    class Meta:
        model = ThematicCategorizationType
        fields = ('id', 'code', 'name')
        
    def get_name(self, instance):
        return _(instance, 'name')

class ClassifierSerializer(serializers.ModelSerializer):
    
    name = serializers.SerializerMethodField()
    
    class Meta:
        model = Classifier
        fields = ('id', 'code', 'name')
        
    def get_name(self, instance):
        return _(instance, 'name')
        
        
 
class SectorSerializer(serializers.ModelSerializer):
    
    name = serializers.SerializerMethodField()
    
    class Meta:
        model = Sector
        fields = ('id', 'code', 'name')
        
    def get_name(self, instance):
        return _(instance, 'name')


class SectorIPCC2006Serializer(serializers.ModelSerializer):
    
    name = serializers.SerializerMethodField()
    
    class Meta:
        model = SectorIPCC2006
        fields = ('id', 'code', 'name', 'sector')
        
    def get_name(self, instance):
        return _(instance, 'name')


class CategoryIPCC2006Serializer(serializers.ModelSerializer):
    
    name = serializers.SerializerMethodField()
    
    class Meta:
        model = CategoryIPCC2006
        fields = ('id', 'code', 'name', 'sector_ipcc_2006')
        
    def get_name(self, instance):
        return _(instance, 'name')


class SubCategoryIPCC2006Serializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    
    class Meta:
        model = SubCategoryIPCC2006
        fields = ('id', 'code', 'name', 'category_ipcc_2006')
    
    def get_name(self, instance):
        return _(instance, 'name')
    

class SectorSelectionSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = SectorSelection
        fields = ('id', 'sector', 'sector_ipcc2006', 'category_ipcc2006',
                  'sub_category_ipcc2006',  'impact_documentation')
    
        
##
## Finish Catalogs Serializers
##


##
## Start Model Serializers
##
## Edit this serializers

class DescarbonizationAxisSelectionSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    class Meta:
        model = DescarbonizationAxisSelection
        fields = ('id', 'descarbonization_axis', 'categorization', 'transformational_vision')
        list_serializer_class = GenericListSerializer
    
    
class ActionAreasSelectionSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    class Meta:
        model = ActionAreasSelection
        fields = ('id', 'area', 'goals', 'categorization')
        list_serializer_class = GenericListSerializer
       

class TopicsSelectionSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    class Meta:
        model = TopicsSelection
        fields = ('id', 'topic', 'sub_topic', 'categorization')
        list_serializer_class = GenericListSerializer
        

class CategorizationSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Categorization
        fields = ('id', 'action_area_selection', 'topics_selection', 'descarbonization_axis_selection', 'impact_category', 'is_part_to_another_mitigation_action', 'relation_description')
    
    def to_representation(self, instance):
        
        data = super().to_representation(instance)
        data['action_area_selection'] = ActionAreasSelectionSerializer(instance.action_area_selection.all(), many=True).data
        data['topics_selection'] = TopicsSelectionSerializer(instance.topics_selection.all(), many=True).data
        data['descarbonization_axis_selection'] = DescarbonizationAxisSelectionSerializer(instance.descarbonization_axis_selection.all(), many=True).data
        data['impact_category'] = ImpactCategorySerializer(instance.impact_category).data

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
                'geographic_coverage', 'other_geographic_coverage', 'disaggregation', 'limitation', 'comments',
                'information_source', 'type_of_data', 'other_type_of_data', 'contact', 'monitoring_information')
    

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


class ChangeLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChangeLog
        fields = ('id', 'date', 'user', 'mitigation_action', 'previous_status', 'current_status')

    def to_representation(self, instance):

        data = super().to_representation(instance)
        ## missing FSM LAbels
        data['date'] = instance.date.strftime('%Y-%m-%d %H:%M:%S')
        data['previous_status'] = f"{data.get('previous_status')} label"
        data['current_status'] = f"{data.get('current_status')} label"
        data['user'] = f'{instance.user.first_name} {instance.user.last_name}'

        return data 


    
class MitigationActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = MitigationAction
        fields = ('id', 'fsm_state','contact', 'code', 'initiative', 'status_information', 'geographic_location', 'categorization','finance', 
                    'ghg_information', 'impact_documentation', 'monitoring_information', 'monitoring_reporting_indicator', 'review_count', 'comments',
                    'user', 'created', 'updated')
        
        # only read code kwargs
        extra_kwargs = {
            'code': {'read_only': True}
        }
          
    
    def _get_fsm_state_info(self, instance):
        data = {
            'state': instance.fsm_state, 
            'label': f'{instance.fsm_state} label'
            ##FSM_STATES.get(instance.fsm_state, f'Error - {instance.fsm_state}')
        }

        return data

    def _next_action(self, instance):

        result = {'states': False, 'required_comments': False}
        # change for transitions method available for users
        transitions = instance.get_available_fsm_state_transitions()
        ## missing label FSM_LABELs
        result = [{'state':transition.target, 'label': f'{transition.target} label', 'required_comments': True} for transition in transitions]

        return result

    def to_representation(self, instance):

        data = super().to_representation(instance)
        data['fsm_state'] = self._get_fsm_state_info(instance)
        data['next_state'] = self._next_action(instance)
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
        data['comments'] = CommentSerializer(instance.comments.filter(fsm_state=instance.fsm_state, review_number=instance.review_count), many=True).data
        data['change_log'] = ChangeLogSerializer(instance.change_log.all().order_by('-date')[0:5], many=True).data
        
        return data



