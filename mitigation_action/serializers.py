from typing import Any

from rest_framework import serializers

from general.utils import get_translation_from_database as _
from mitigation_action.models import (
    ActionAreas,
    ActionAreasSelection,
    ActionGoals,
    Activity,
    CarbonDeposit,
    Categorization,
    CategoryIPCC2006,
    ChangeLog,
    Classifier,
    Contact,
    DescarbonizationAxis,
    DescarbonizationAxisSelection,
    Finance,
    FinanceInformation,
    FinanceSourceType,
    FinanceStatus,
    GenericFileStorage,
    GeographicLocation,
    GeographicScale,
    GHGImpactSector,
    GHGInformation,
    ImpactCategory,
    ImpactDocumentation,
    Indicator,
    IndicatorChangeLog,
    InformationSource,
    InformationSourceType,
    Initiative,
    InitiativeGoal,
    InitiativeType,
    MitigationAction,
    MitigationActionStatus,
    MonitoringIndicator,
    MonitoringInformation,
    MonitoringReportingIndicator,
    QAQCReductionEstimateQuestion,
    Sector,
    SectorIPCC2006,
    SectorSelection,
    Standard,
    Status,
    SubCategoryIPCC2006,
    SubTopics,
    SustainableDevelopmentGoals,
    ThematicCategorizationType,
    Topics,
    TopicsSelection,
    TransformationalVisions,
    CategoryOption,
    CategoryResult,
    Scale,
    Results,
    OtherOption,
    CategorySection,
    SpecificImpact,
    Processes
)

from general.serializers import CategoryCTSerializer, CategorySerializer, CharacteristicSerializer
from workflow.serializers import CommentSerializer

from .constants import MitigationActionFilesType
from .workflow.services import MitigationActionWorkflowStep
from .workflow.states import FSM_STATE_TRANSLATION

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

class FileStorageSerializer(serializers.ModelSerializer):
    class Meta:
        model = GenericFileStorage
        fields = (
            'id',
            'file',
            'type',
            'metadata'
        )

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
        fields = (
            "id",
            "code",
            "name",
        )

    def get_name(self, instance):
        return _(instance, "name")


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
    id = serializers.IntegerField()

    class Meta:
        model = SectorSelection
        fields = (
            "id",
            "sector",
            "sector_ipcc_2006",
            "category_ipcc_2006",
            "sub_category_ipcc_2006",
            "impact_documentation",
        )
        list_serializer_class = GenericListSerializer

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["sector"] = SectorSerializer(instance.sector).data
        data["sector_ipcc_2006"] = SectorIPCC2006Serializer(
            instance.sector_ipcc_2006
        ).data
        data["category_ipcc_2006"] = CategoryIPCC2006Serializer(
            instance.category_ipcc_2006
        ).data
        data["sub_category_ipcc_2006"] = SubCategoryIPCC2006Serializer(
            instance.sub_category_ipcc_2006.all(), many=True
        ).data

        return data
        
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
    
    def to_representation(self, instance):
        data =  super().to_representation(instance)
        data['descarbonization_axis'] = DescarbonizationAxisSerializer(instance.descarbonization_axis).data
        data['transformational_vision'] = TransformationalVisionsSerializer(instance.transformational_vision.all(), many=True).data
        return data
    
    
class ActionAreasSelectionSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    class Meta:
        model = ActionAreasSelection
        fields = ('id', 'area', 'goals', 'categorization')
        list_serializer_class = GenericListSerializer
    
    def to_representation(self, instance):
        data =  super().to_representation(instance)
        data['area'] = ActionAreasSerializer(instance.area).data
        data['goals'] = ActionGoalsSerializer(instance.goals.all(), many=True).data
        return data
       

class TopicsSelectionSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    class Meta:
        model = TopicsSelection
        fields = ('id', 'topic', 'sub_topic', 'categorization')
        list_serializer_class = GenericListSerializer
    
    def to_representation(self, instance):
        data =  super().to_representation(instance)
        data['topic'] = TopicsSerializer(instance.topic).data
        data['sub_topic'] = SubTopicsSerializer(instance.sub_topic.all(), many=True).data
        return data
        

class CategorizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categorization
        fields = (
            "id",
            "action_area_selection",
            "topics_selection",
            "descarbonization_axis_selection",
            "impact_category",
            "is_part_to_another_mitigation_action",
            "relation_description",
        )

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
        fields = ('id', 'code', 'question', 'is_checked', 'detail', 'impact_documentation')
        list_serializer_class = GenericListSerializer


class MonitoringIndicatorSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    files = FileStorageSerializer(many=True, read_only=True)
    class Meta:
        model = MonitoringIndicator
        fields = (
            "id",
            "initial_date_report_period",
            "final_date_report_period",
            "data_updated_date",
            "report_type",
            "updated_data",
            "report_line_text",
            "web_service_conection",
            "progress_report_period",
            "progress_report_period_until",
            "progress_report",
            "indicator",
            "monitoring_reporting_indicator",
            "files",
        )
        list_serializer_class = GenericListSerializer

    def to_representation(self, instance):
        data = super().to_representation(instance)

        if instance.indicator:
            data['indicator'] = instance.indicator.name
        return data


        

class IndicatorChangeLogSerializer(serializers.ModelSerializer):

    class Meta:
        model = IndicatorChangeLog
        fields = ('id', 'indicator', 'update_date', 'changes', 'changes_description', 'author')



class IndicatorSerializer(serializers.ModelSerializer):
    files = FileStorageSerializer(many=True, read_only=True)
    class Meta:
        model = Indicator
        fields = (
            "id",
            "name",
            "description",
            "mitigation_action",
            "unit",
            "methodological_detail",
            "reporting_periodicity",
            "available_time_start_date",
            "available_time_end_date",
            "ghg_indicator_goal",
            "ghg_indicator_base",
            "geographic_coverage",
            "other_geographic_coverage",
            "disaggregation",
            "limitation",
            "classifier",
            "other_classifier",
            "ensure_sustainability",
            "comments",
            "information_source",
            "type_of_data",
            "other_type_of_data",
            "contact",
            "monitoring_information",
            "files",
        )

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['contact'] = ContactSerializer(instance.contact).data
        data['information_source'] = InformationSourceSerializer(instance.information_source).data
        data['change_log'] = IndicatorChangeLogSerializer(instance.indicator_change_log.all(), many=True).data
        data['classifier'] = ClassifierSerializer(instance.classifier.all(), many=True).data
        ## push the indicator_id to the indicator_change_log
        return data


class InformationSourceSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = InformationSource
        fields = ('id', 'responsible_institution', 'type', 'other_type', 'statistical_operation')
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['type'] = InformationSourceTypeSerializer(instance.type.all(), many=True).data
        
        return data
    


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
        fields = (
            "id",
            "estimate_reduction_co2",
            "period_potential_reduction",
            "base_line_definition",
            "carbon_deposit",
            "gases",
            "calculation_methodology",
            "estimate_calculation_documentation",
            "mitigation_action_in_inventory",
            "standard",
            "other_standard",
            "carbon_international_commerce",
            "methodologies_to_use",
        )

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["question"] = QAQCReductionEstimateQuestionSerializer(
            instance.question.all(), many=True
        ).data
        data["carbon_deposit"] = CarbonDepositSerializer(
            instance.carbon_deposit.all(), many=True
        ).data
        data["standard"] = StandardSerializer(instance.standard).data
        data["sector_selection"] = SectorSelectionSerializer(
            instance.sector_selection.all(), many=True
        ).data

        return data


class GHGInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = GHGInformation
        fields = (
            "id",
            "impact_emission",
            "graphic_description",
            "impact_sector",
            "goals",
        )

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["impact_sector"] = GHGImpactSectorSerializer(
            instance.impact_sector.all(), many=True
        ).data
        data["goals"] = SustainableDevelopmentGoalsSerializer(
            instance.goals.all(), many=True
        ).data

        return data


class FinanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Finance
        fields = (
            "id",
            "status",
            "administration",
            "source",
            "mideplan_registered",
            "mideplan_project",
            "executing_entity",
        )

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["status"] = FinanceStatusSerializer(instance.status).data
        data["source"] = FinanceSourceTypeSerializer(instance.source.all(), many=True).data
        data["finance_information"] = FinanceInformationSerializer(instance.finance_information.all(), many=True).data

        return data


class FinanceInformationSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = FinanceInformation
        fields = (
            "id",
            "source_description",
            "budget",
            "currency",
            "finance",
            "reference_year",
        )
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
        fields = (
            "id",
            "name",
            "objective",
            "description",
            "initiative_type",
        )

    def to_representation(self, instance):

        data = super().to_representation(instance)
        data['initiative_type'] = InitiativeTypeSerializer(instance.initiative_type).data
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
        fields = (
            "id",
            "institution",
            "full_name",
            "job_title",
            "email",
            "phone",
            "user",
            "created",
            "updated",
        )


class ChangeLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChangeLog
        fields = (
            "id",
            "date",
            "user",
            "mitigation_action",
            "previous_status",
            "current_status",
        )

    def to_representation(self, instance):

        data = super().to_representation(instance)
        ## missing FSM LAbels
        data['date'] = instance.date.strftime('%Y-%m-%d %H:%M:%S')
        data['previous_status'] = _(FSM_STATE_TRANSLATION.get(data.get('previous_status')), 'label')
        data['current_status'] = _(FSM_STATE_TRANSLATION.get(data.get('current_status')), 'label')
        data['user'] = f'{instance.user.first_name} {instance.user.last_name}'

        return data 


    




"""
In the future we need to split this serializers in different files,
for example:
- catalogs.py
- mitigation_action.py
- indicators.py
- monitoring.py
- finance.py
- etc.
This will help to keep the code organized and maintainable.

"""
## Serializers Models
# Files

##Section 7-8

class IndicatorResumeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Indicator
        fields = ('id', 'name', 'description')


class OtherOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = OtherOption
        fields = ('id', 'name', 'description', 'indicator', 'base_value', 'expected_value', 'accumulated_value', 'created', 'updated')

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['indicator'] = IndicatorResumeSerializer(instance.indicator).data
        return data


class CategorySectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategorySection
        fields = ('id', 'category', 'indicator', 'base_value', 'expected_value', 'accumulated_value', 'description', 'created', 'updated')

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['category'] = CategorySerializer(instance.category).data
        data['indicator'] = IndicatorResumeSerializer(instance.indicator).data
        return data


class CategoryOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryOption
        fields = ('id','category_section','other','impact_type','pertinent','relevant','created', 'updated')

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['category_section'] = CategorySectionSerializer(instance.category_section.all(), many=True).data
        data['other'] = OtherOptionSerializer(instance.other.all(), many=True).data
        return data


class CategoryResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryResult
        fields = ('id', 'code', 'name', 'created', 'updated')


class ScaleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Scale
        fields = ('id','code','name','description','category_result','indicator', 'base_value', 'expected_value', 'accumulated_value','created','updated')

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['category_result'] = CategoryResultSerializer(instance.category_result.all(), many=True).data
        data['indicator'] = IndicatorResumeSerializer(instance.indicator).data

        return data


class ResultsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Results
        fields = ('id', 'scale', 'created', 'updated')

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['scale'] = ScaleSerializer(instance.scale.all(), many=True).data

        return data


class SpecificImpactSerializer(serializers.ModelSerializer):

    class Meta:
        model = SpecificImpact
        fields = ('id', 'category_ct', 'description','indicator', 'base_value', 'expected_value', 'accumulated_value', 'created', 'updated')

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['category_ct'] = CategoryCTSerializer(instance.category_ct).data
        data['indicator'] = IndicatorResumeSerializer(instance.indicator).data
        return data


class ProcessesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Processes
        fields = ('id', 'characteristic', 'other', 'specific_impact', 'created', 'updated')

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['characteristic'] = CharacteristicSerializer(instance.characteristic.all(), many=True).data
        data['specific_impact'] = SpecificImpactSerializer(instance.specific_impact.all(), many=True).data
        return data

## Main Serializer
class MitigationActionSerializer(serializers.ModelSerializer):
    files = FileStorageSerializer(many=True, read_only=True)
    class Meta:
        model = MitigationAction
        fields = (
            "id",
            "fsm_state",
            "contact",
            "code",
            "initiative",
            "status_information",
            "geographic_location",
            "categorization",
            "finance",
            "ghg_information",
            "impact_documentation",
            "monitoring_information",
            "monitoring_reporting_indicator",
            "review_count",
            "result",
            "category_option",
            "process",
            "final_result",
            "comments",
            "user",
            "files",
            "created",
            "updated",
        )

        # only read code kwargs
        extra_kwargs = {"code": {"read_only": True}}
          
    
    def _get_fsm_state_info(self, instance):
        data = {
            'state': instance.fsm_state, 
            'label': _(FSM_STATE_TRANSLATION.get(instance.fsm_state), 'label')
        }

        return data

    def _next_action(self, instance):
        _workflow_service = MitigationActionWorkflowStep(mitigation_action=instance)

        return [
            {
                'state':state,
                'label': _(FSM_STATE_TRANSLATION.get(state), 'label'),
                'required_comments': True
            } for state in _workflow_service.get_next_states() 
        ]

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
        data['result'] = ResultsSerializer(instance.result.all(), many=True).data
        data['category_option'] = CategoryOptionSerializer(instance.category_option).data
        data['process'] = ProcessesSerializer(instance.process).data
        data['final_result'] = ResultsSerializer(instance.final_result.all(), many=True).data
        data['comments'] = CommentSerializer(instance.comments.filter(fsm_state=instance.fsm_state, review_number=instance.review_count), many=True).data
        data['change_log'] = ChangeLogSerializer(instance.change_log.all().order_by('-date')[0:5], many=True).data
        
        return data
    

class MitigationActionListSerializer(serializers.ModelSerializer):
    fsm_state = serializers.SerializerMethodField()
    next_state = serializers.SerializerMethodField()
    type = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    class Meta:
        model = MitigationAction
        fields = (
            "id",
            "fsm_state",
            "type",
            "name",
            "next_state",
            "code",
            "review_count",
            "user",
            "created",
            "updated",
        )
        # only read code kwargs
        extra_kwargs = {"code": {"read_only": True}}

    def _get_fsm_state_info(self, instance):
        data = {
            'state': instance.fsm_state, 
            'label': _(FSM_STATE_TRANSLATION.get(instance.fsm_state), 'label')
        }

        return data

    def get_fsm_state(self, instance):
        """
        Returns the FSM state information for the Mitigation Action instance.
        """
        return self._get_fsm_state_info(instance)

    def get_next_state(self, instance):
        """
        Returns the next possible states for the Mitigation Action instance.
        """
        _workflow_service = MitigationActionWorkflowStep(mitigation_action=instance)

        return [
            {
                'state': state,
                'label': _(FSM_STATE_TRANSLATION.get(state), 'label'),
                'required_comments': True
            } for state in _workflow_service.get_next_states()
        ]

    def get_type(self, instance):
        """
        Returns the type of the Mitigation Action instance.
        """
        if instance.initiative:
            name = _(instance.initiative.initiative_type, 'name')
            return f"{instance.initiative.initiative_type.type} - {name}"
        
        return None

    def get_name(self, instance):
        """
        Returns the name of the Mitigation Action instance.
        """
        if instance.initiative:
            return instance.initiative.name
        
        return None



## Serializers to validate request data
## Files
class FileListRequestBodySerializer(serializers.Serializer):
    files = serializers.ListField(
        child=serializers.FileField(),
        max_length=10,  
        min_length=1,  
        
    )
    type = serializers.ChoiceField(
        choices=MitigationActionFilesType.values()
    )
    entity_id = serializers.CharField(
        required=False
    )
    entity_type = serializers.ChoiceField(
        choices=MitigationActionFilesType.get_entity_types(), required=False
    )

    def validate(self, data: dict[str, Any]) -> dict[str, Any]:
        if MitigationActionFilesType.get_entity_types_from_value(
            data.get("type")
        ) != data.get("entity_type", 'mitigation-action'):
            raise serializers.ValidationError(
                f"Invalid 'type' value. Must be one of: {MitigationActionFilesType.get_entity_types()}"
            )
        if bool(data.get('entity_type')) != bool(data.get('entity_id')):
            raise serializers.ValidationError(
                "Both 'entity_type' and 'entity_id' must be provided together or not at all."
            )
        
      
        return data


class GetFilesListRequestBodySerializer(serializers.Serializer):
    entity_type = serializers.ChoiceField(
        choices=MitigationActionFilesType.get_entity_types(), required=False
    )
    entity_id = serializers.CharField(
        required=False
    )


    def validate(self, data: dict[str, Any]) -> dict[str, Any]:
        if bool(data.get('entity_type')) != bool(data.get('entity_id')):
            raise serializers.ValidationError(
                "Both 'entity_type' and 'entity_id' must be provided together or not at all."
            )
        return data