
from asyncio import start_unix_server
from os import error

from django_fsm import has_transition_perm
from adaptation_action.models import ReportOrganization, AdaptationAction
from adaptation_action.serializers import *
from general.helpers.services import ServiceHelper
from general.helpers.serializer import SerializersHelper
from general.serializers import DistrictSerializer

class AdaptationActionServices():
    def __init__(self) -> None:

        self._service_helper = ServiceHelper()
        self._serializer_helper = SerializersHelper()
        self.FUNCTION_INSTANCE_ERROR = 'Error Adaptation Action Service does not have {0} function'
        self.ATTRIBUTE_INSTANCE_ERROR = 'Instance Model does not have {0} attribute'
        self.INVALID_STATUS_TRANSITION = "Invalid adaptation action state transition."
        self.STATE_HAS_NO_AVAILABLE_TRANSITIONS = "State has no available transitions."


    def _create_sub_record(self, data, sub_record_name):
        
        create_function = f'_create_update_{sub_record_name}'

        if hasattr(self, create_function):
            function = getattr(self, create_function)
            record_status, record_detail = function(data=data)
            result = (record_status, record_detail)
        
        else:
            raise Exception(self.FUNCTION_INSTANCE_ERROR.format(create_function))

        return result
    
    def _update_sub_record(self, sub_record_name, record_for_updating, data):
        
        update_function = f'_create_update_{sub_record_name}'
        
        if hasattr(self, update_function):
          
            function = getattr(self, update_function)
        
            record_status, record_detail = function(data, record_for_updating)
          
            result = (record_status, record_detail)
        
        else:
            raise Exception(self.FUNCTION_INSTANCE_ERROR.format(update_function))

        return result

    def _create_or_update_record(self, instance, field, data):

        result = (False, [])
        if hasattr(instance, field):
            if getattr(instance, field) == None:
                record_status, record_data = self._create_sub_record(data, field) ## field = sub_record_name

            else:
                ## change field(string) to object(model instance)
                record_for_updating = getattr(instance, field) 
                record_status, record_data = self._update_sub_record(field, record_for_updating, data)
            
            result = (record_status, record_data)
        else:

            result = (False, self.ATTRIBUTE_INSTANCE_ERROR)

        return result

    def _get_serialized_adaptation_action(self, data, adaptation_action = False):

        serializer = self._serializer_helper.get_serialized_record(AdaptationActionSerializer, data, record=adaptation_action)

        return serializer
    
    def _get_serialized_report_organization(self, data, report_organization = False):

        serializers = self._serializer_helper.get_serialized_record(ReportOrganizationSerializer, data, record=report_organization)

        return serializers

    def _get_serialized_progress_log(self, data, progress_log = False):

        serializers = self._serializer_helper.get_serialized_record(ProgressLogSerializer, data, record=progress_log)

        return serializers
    
    def _get_serialized_indicator_source(self, data, indicator_source = False):

        serializers = self._serializer_helper.get_serialized_record(IndicatorSourceSerializer, data, record=indicator_source)

        return serializers
    
    def _get_serialized_indicator_monitoring(self, data, indicator_monitoring = False):

        serializers = self._serializer_helper.get_serialized_record(IndicatorMonitoringSerializer, data, record=indicator_monitoring)

        return serializers
    
    def _get_serialized_general_report(self, data, general_report = False):

        serializers = self._serializer_helper.get_serialized_record(GeneralReportSerializer, data, record=general_report)

        return serializers
    
    def _get_serialized_action_impact(self, data, action_impact = False):

        serializers = self._serializer_helper.get_serialized_record(ActionImpactSerializer, data, record=action_impact)

        return serializers
    
    def _create_update_progress_log(self, data, progress_log=False):

        if progress_log:
            serialized_progress_log = self._get_serialized_progress_log(data, progress_log)
        
        else:
            serialized_progress_log = self._get_serialized_progress_log(data)
        
        if serialized_progress_log.is_valid():
            progress_log = serialized_progress_log.save()
            result = (True, progress_log)
        
        else:
            result = (False, serialized_progress_log.errors)

        return result
    
    def _create_update_indicator_monitoring(self, data, indicator_monitoring=False):

        if indicator_monitoring:
            serialized_indicator_monitoring = self._get_serialized_indicator_monitoring(data, indicator_monitoring)
        
        else:
            serialized_indicator_monitoring = self._get_serialized_indicator_monitoring(data)
        
        if serialized_indicator_monitoring.is_valid():
            indicator_monitoring = serialized_indicator_monitoring.save()
            result = (True, indicator_monitoring)
        
        else:
            result = (False, serialized_indicator_monitoring.errors)
        
        return result

    def _create_update_general_report(self, data, general_report=False):

        if general_report:
            serialized_general_report = self._get_serialized_general_report(data, general_report)
        
        else:
            serialized_general_report = self._get_serialized_general_report(data)
        
        if serialized_general_report.is_valid():
            general_report = serialized_general_report.save()
            result = (True, general_report)
        
        else:
            result = (False, serialized_general_report.errors)

        return result
    
    def _create_update_action_impact(self, data, action_impact=False):

        if action_impact:
            serialized_action_impact = self._get_serialized_action_impact(data, action_impact)
        
        else:
            serialized_action_impact = self._get_serialized_action_impact(data)
        
        if serialized_action_impact.is_valid():
            action_impact = serialized_action_impact.save()
            result = (True, action_impact)
        
        else:
            result = (False, serialized_action_impact.errors)

        return result

    def _get_serialized_report_organization_type(self, data, report_organization_type = False):

        serializers = self._serializer_helper.get_serialized_record(ReportOrganizationTypeSerializer, data, record=report_organization_type)

        return serializers
    
    def _get_serialized_adaptation_action_type(self, data, adaptation_action_type = False):

        serializers = self._serializer_helper.get_serialized_record(AdaptationActionTypeSerializer, data, record=adaptation_action_type)

        return serializers
    
    def _get_serialized_ODS(self, data, ODS=False):

        serializer = self._serializer_helper.get_serialized_record(ODSSerializer, data, record=ODS)

        return serializer
    
    def _get_serialized_adaptation_action_information(self, data, adaptation_action_information = False):

        serializer = self._serializer_helper.get_serialized_record(AdaptationActionInformationSerializer, data, record=adaptation_action_information)

        return serializer
    
    def _get_serialized_topics(self, data, topics = False):

        serializer = self._serializer_helper.get_serialized_record(TopicsSerializer, data, record=topics)

        return serializer
    
    def _get_serialized_sub_topics(self, data, subtopics = False):

        serializer = self._serializer_helper.get_serialized_record(SubTopicsSerializer, data, record=subtopics)

        return serializer
    
    def _get_serialized_adaptation_axis(self, data, adaptation_axis = False):

        serializer = self._serializer_helper.get_serialized_record(AdaptationAxisSerializer, data, record=adaptation_axis)

        return serializer
    
    def _get_serialized_adaptation_axis_guideline(self, data, adaptation_axis_guideline = False):

        serializer = self._serializer_helper.get_serialized_record(AdaptationAxisGuidelineSerializer, data, record=adaptation_axis_guideline)

        return serializer
    
    def _get_serialized_NDC_area(self, data, NDC_area = False):

        serializer = self._serializer_helper.get_serialized_record(NDCAreaSerializer, data, record=NDC_area)

        return serializer
    
    def _get_serialized_NDC_contribution(self, data, NDC_contribution = False):

        serializer = self._serializer_helper.get_serialized_record(NDCContributionSerializer, data, record=NDC_contribution)

        return serializer
    
    def _get_serialized_activity(self, data, activity = False):

        serializer = self._serializer_helper.get_serialized_record(ActivitySerializer, data, record=activity)

        return serializer
    
    def _get_serialized_instrument(self, data, instrument = False):

        serializer = self._serializer_helper.get_serialized_record(InstrumentSerializer, data, record=instrument)

        return serializer
    
    def _get_serialized_type_climate_threat(self, data, type_climate_threat = False):

        serializer = self._serializer_helper.get_serialized_record(TypeClimateThreatSerializer, data, record=type_climate_threat)

        return serializer
    
    def _get_serialized_climate_threat(self, data, climate_threat = False):

        serializer = self._serializer_helper.get_serialized_record(ClimateThreatSerializer, data, record=climate_threat)

        return serializer
    
    def _get_serialized_implementation(self, data, implementation = False):

        serializer = self._serializer_helper.get_serialized_record(ImplementationSerializer, data, record=implementation)

        return serializer

    def _get_serialized_finance_adaptation(self, data, finance = False):

        serializer = self._serializer_helper.get_serialized_record(FinanceSerializer, data, record=finance)

        return serializer
    
    def _get_serialized_status(self, data, status=False):

        serializer = self._serializer_helper.get_serialized_record(StatusSerializer, data, record=status)

        return serializer
    
    def _get_serialized_mideplan(self, data, mideplan=False):

        serializer = self._serializer_helper.get_serialized_record(MideplanSerializer, data, record=mideplan)

        return serializer
    
    def _get_serialized_information_source(self, data, information_source=False):

        serializer = self._serializer_helper.get_serialized_record(InformationSourceSerializer, data, record=information_source)
        
        return serializer

    def _get_serialized_indicator_adaptation(self, data, indicator_adaptation=False):

        serializer = self._serializer_helper.get_serialized_record(IndicatorSerializer, data, record=indicator_adaptation)

        return serializer
    
    def _create_update_address(self, data, address=False):
        
        if address:
            serializer = self._serializer_helper.get_serialized_record(AddressSerializer, data, record=address)
        else:
            serializer = self._serializer_helper.get_serialized_record(AddressSerializer, data)

        if serializer.is_valid():
            address = serializer.save()
            result = (True, address)
        
        else:
            result = (False, serializer.errors)

        return result

    def _create_update_report_organization_type(self, data, report_organization_type = False):

        if report_organization_type:
            serialized_report_organization_type = self._get_serialized_report_organization_type(data, report_organization_type)
        
        else:
            serialized_report_organization_type = self._get_serialized_report_organization_type(data)
        
        if serialized_report_organization_type.is_valid():
            report_organization_type = serialized_report_organization_type.save()
            result = (True, report_organization_type)
        
        else:
            result = (False, serialized_report_organization_type.errors)
        
        return result
    
    def _create_update_adaptation_action_type(self, data, adaptation_action_type = False):

        if adaptation_action_type:
            serialized_adaptation_action_type = self._get_serialized_adaptation_action_type(data, adaptation_action_type)
        
        else:
            serialized_adaptation_action_type = self._get_serialized_adaptation_action_type(data)
        
        if serialized_adaptation_action_type.is_valid():
            adaptation_action_type = serialized_adaptation_action_type.save()
            result = (True, adaptation_action_type)
        
        else:
            result = (False, serialized_adaptation_action_type.errors)
        
        return result

    def _create_update_ODS(self, data, ODS=False):
            
            if ODS:
                serialized_ODS = self._get_serialized_ODS(data, ODS)
            
            else:
                serialized_ODS = self._get_serialized_ODS(data)
            
            if serialized_ODS.is_valid():
                ODS = serialized_ODS.save()
                result = (True, ODS)
            
            else:
                result = (False, serialized_ODS.errors)
            
            return result
    
    def _create_update_adaptation_action_information(self, data, adaptation_action_information = False):
            
            if adaptation_action_information:
                serialized_adaptation_action_information = self._get_serialized_adaptation_action_information(data, adaptation_action_information)
            
            else:
                serialized_adaptation_action_information = self._get_serialized_adaptation_action_information(data)
            
            if serialized_adaptation_action_information.is_valid():
                adaptation_action_information = serialized_adaptation_action_information.save()
                result = (True, adaptation_action_information)
            
            else:
                result = (False, serialized_adaptation_action_information.errors)
            
            return result
    
    def _create_update_adaptation_action_information(self, data, adaptation_action_information = False):
            
            if adaptation_action_information:
                serialized_adaptation_action_information = self._get_serialized_adaptation_action_information(data, adaptation_action_information)
            
            else:
                serialized_adaptation_action_information = self._get_serialized_adaptation_action_information(data)
            
            if serialized_adaptation_action_information.is_valid():
                adaptation_action_information = serialized_adaptation_action_information.save()
                result = (True, adaptation_action_information)
            
            else:
                result = (False, serialized_adaptation_action_information.errors)
            
            return result
    
    def _create_update_topics(self, data, topic = False):
            
            if topic:
                serialized_topic = self._get_serialized_topic(data, topic)
            
            else:
                serialized_topic = self._get_serialized_topic(data)
            
            if serialized_topic.is_valid():
                topic = serialized_topic.save()
                result = (True, topic)
            
            else:
                result = (False, serialized_topic.errors)
            
            return result
    
    def _create_update_sub_topics(self, data, sub_topic = False):
            
            if sub_topic:
                serialized_sub_topic = self._get_serialized_sub_topic(data, sub_topic)
            
            else:
                serialized_sub_topic = self._get_serialized_sub_topic(data)
            
            if serialized_sub_topic.is_valid():
                sub_topic = serialized_sub_topic.save()
                result = (True, sub_topic)
            
            else:
                result = (False, serialized_sub_topic.errors)
            
            return result
    
    def _create_update_adaptation_axis(self, data, adaptation_axis = False):
            
            if adaptation_axis:
                serialized_adaptation_axis = self._get_serialized_adaptation_axis(data, adaptation_axis)
            
            else:
                serialized_adaptation_axis = self._get_serialized_adaptation_axis(data)
            
            if serialized_adaptation_axis.is_valid():
                adaptation_axis = serialized_adaptation_axis.save()
                result = (True, adaptation_axis)
            
            else:
                result = (False, serialized_adaptation_axis.errors)
            
            return result
    
    def _create_update_adaptation_axis_guideline(self, data, adaptation_axis_guideline = False):
            
            if adaptation_axis_guideline:
                serialized_adaptation_axis_guideline = self._get_serialized_adaptation_axis_guideline(data, adaptation_axis_guideline)
            
            else:
                serialized_adaptation_axis_guideline = self._get_serialized_adaptation_axis_guideline(data)
            
            if serialized_adaptation_axis_guideline.is_valid():
                adaptation_axis_guideline = serialized_adaptation_axis_guideline.save()
                result = (True, adaptation_axis_guideline)
            
            else:
                result = (False, serialized_adaptation_axis_guideline.errors)
            
            return result
    
    def _create_update_NDC_area(self, data, NDC_area = False):
            
            if NDC_area:
                serialized_NDC_area = self._get_serialized_NDC_area(data, NDC_area)
            
            else:
                serialized_NDC_area = self._get_serialized_NDC_area(data)
            
            if serialized_NDC_area.is_valid():
                NDC_area = serialized_NDC_area.save()
                result = (True, NDC_area)
            
            else:
                result = (False, serialized_NDC_area.errors)
            
            return result
    
    def _create_update_NDC_contribution(self, data, NDC_contribution = False):
            
            if NDC_contribution:
                serialized_NDC_contribution = self._get_serialized_NDC_contribution(data, NDC_contribution)
            
            else:
                serialized_NDC_contribution = self._get_serialized_NDC_contribution(data)
            
            if serialized_NDC_contribution.is_valid():
                NDC_contribution = serialized_NDC_contribution.save()
                result = (True, NDC_contribution)
            
            else:
                result = (False, serialized_NDC_contribution.errors)
            
            return result
    
    def _create_update_activity(self, data, activity = False):
            
            if activity:
                serialized_activity = self._get_serialized_activity(data, activity)
            
            else:
                serialized_activity = self._get_serialized_activity(data)
            
            if serialized_activity.is_valid():
                activity = serialized_activity.save()
                result = (True, activity)
            
            else:
                result = (False, serialized_activity.errors)
            
            return result
    
    def _create_update_instrument(self, data, instrument = False):
            
            if instrument:
                serialized_instrument = self._get_serialized_instrument(data, instrument)
            
            else:
                serialized_instrument = self._get_serialized_instrument(data)
            
            if serialized_instrument.is_valid():
                instrument = serialized_instrument.save()
                result = (True, instrument)
            
            else:
                result = (False, serialized_instrument.errors)
            
            return result
    
    def _create_update_type_climate_threat(self, data, type_climate_threat = False):
            
            if type_climate_threat:
                serialized_type_climate_threat = self._get_serialized_type_climate_threat(data, type_climate_threat)
            
            else:
                serialized_type_climate_threat = self._get_serialized_type_climate_threat(data)
            
            if serialized_type_climate_threat.is_valid():
                type_climate_threat = serialized_type_climate_threat.save()
                result = (True, type_climate_threat)
            
            else:
                result = (False, serialized_type_climate_threat.errors)
            
            return result
    
    def _create_update_climate_threat(self, data, climate_threat = False):
            
            if climate_threat:
                serialized_climate_threat = self._get_serialized_climate_threat(data, climate_threat)
            
            else:
                serialized_climate_threat = self._get_serialized_climate_threat(data)
            
            if serialized_climate_threat.is_valid():
                climate_threat = serialized_climate_threat.save()
                result = (True, climate_threat)
            
            else:
                result = (False, serialized_climate_threat.errors)
            
            return result
    
    def _create_update_implementation(self, data, implementation = False):
            
            if implementation:
                serialized_implementation = self._get_serialized_implementation(data, implementation)
            
            else:
                serialized_implementation = self._get_serialized_implementation(data)
            
            if serialized_implementation.is_valid():
                implementation = serialized_implementation.save()
                result = (True, implementation)
            
            else:
                result = (False, serialized_implementation.errors)
            
            return result
    
    def _create_update_finance(self, data, finance_adaptation = False):
        
        _status = data.pop('status', None)
        _mideplan = data.pop('mideplan', None)

        if(_status):

            serialized_status = self._get_serialized_status(_status)

            if(serialized_status.is_valid()):
                status = serialized_status.save()
                data['status'] = status.id

        if(_mideplan):

            serialized_mideplan = self._get_serialized_mideplan(_mideplan)

            if(serialized_mideplan.is_valid()):
                mideplan = serialized_mideplan.save()
                data['mideplan'] = mideplan.id

        if finance_adaptation:
            serialized_finance = self._get_serialized_finance_adaptation(data, finance_adaptation)
        
        else:
            serialized_finance = self._get_serialized_finance_adaptation(data)
        
        if serialized_finance.is_valid():
            finance_adaptation = serialized_finance.save()
            result = (True, finance_adaptation)
        
        else:
            result = (False, serialized_finance.errors)
        
        return result
    
    def _create_update_status(self, data, status = False):

        if status:
            serialized_status = self._get_serialized_status(data, status)
        
        else:
            serialized_status = self._get_serialized_status(data)
        
        if serialized_status.is_valid():
            status = serialized_status.save()
            result = (True, status)
        
        else:
            result = (False, serialized_status.errors)
        
        return result
            
    def _create_update_information_source(self, data, information_source=False):

        if information_source:
            serialized_information_source = self._get_serialized_information_source(data, information_source)
        
        else:
            serialized_information_source = self._get_serialized_information_source(data)
        
        if serialized_information_source.is_valid():
            information_source = serialized_information_source.save()
            result = (True, information_source)
        
        else:
            result = (False, serialized_information_source.errors)
        
        return result

    def _create_update_indicator(self, data, indicator_adaptation=False):

        _information_source = data.pop('information_source', None)

        if(_information_source):
                
            serialized_information_source = self._get_serialized_information_source(_information_source)

            if(serialized_information_source.is_valid()):
                information_source = serialized_information_source.save()
                data['information_source'] = information_source.id

        if indicator_adaptation:
            serialized_indicator_adaptation = self._get_serialized_indicator_adaptation(data, indicator_adaptation)
        
        else:
            serialized_indicator_adaptation = self._get_serialized_indicator_adaptation(data)
        
        if serialized_indicator_adaptation.is_valid():
            indicator_adaptation = serialized_indicator_adaptation.save()
            result = (True, indicator_adaptation)
        
        else:
            result = (False, serialized_indicator_adaptation.errors)
        
        return result

    def _create_update_report_organization(self, data, report_organization=False):

        if report_organization:
            serialized_report_organization = self._get_serialized_report_organization(data, report_organization)
        
        else:
            serialized_report_organization = self._get_serialized_report_organization(data)
        
        if serialized_report_organization.is_valid():
            report_organization = serialized_report_organization.save()
            result = (True, report_organization)
        
        else:
            result = (False, serialized_report_organization.errors)

        return result

    def _get_all_type_climate_threat(self, request):

        climate_status, climate_data = self._service_helper.get_all(TypeClimateThreat)

        if climate_status:
            result = (climate_status, TypeClimateThreatSerializer(climate_data, many=True).data)
        
        else:
            result = (climate_status, climate_data)
        
        return result
    
    def _get_all_ods(self, request):

        ods_status, ods_data = self._service_helper.get_all(ODS)

        if ods_status:
            result = (ods_status, ODSSerializer(ods_data, many=True).data)
        
        else:
            result = (ods_status, ods_data)
        
        return result
    
    def _get_all_topic(self, request):

        topic_status, topic_data = self._service_helper.get_all(Topics)

        if topic_status:
            result = (topic_status, TopicsSerializer(topic_data, many=True).data)
        
        else:
            result = (topic_status, topic_data)
        
        return result

    def _get_topic_by_id(self, request):
        
        topic_id = request.GET.get('topic_id')
        topic_status, topic_data = self._service_helper.get_by_id(topic_id, Topics)

        if topic_status:
            result = (topic_status, TopicsSerializer(topic_data).data)
        
        else:
            result = (topic_status, topic_data)
        
        return result
    
    def _get_all_subtopic(self, request):

        subtopic_status, subtopic_data = self._service_helper.get_all(SubTopics)

        if subtopic_status:
            result = (subtopic_status, SubTopicsSerializer(subtopic_data, many=True).data)
        
        else:
            result = (subtopic_status, subtopic_data)
        
        return result
    
    def _get_subtopic_by_id(self, request):

        subtopic_id = request.GET.get('subtopic_id')
        subtopic_status, subtopic_data = self._service_helper.get_by_id(subtopic_id, SubTopics)

        if subtopic_status:
            result = (subtopic_status, SubTopicsSerializer(subtopic_data).data)
        
        else:
            result = (subtopic_status, subtopic_data)
        
        return result

    def _get_all_source_type(self, request):
            
        source_type_status, source_type_data = self._service_helper.get_all(InformationSourceType)

        if source_type_status:
            result = (source_type_status, InformationSourceTypeSerializer(source_type_data, many=True).data)
        
        else:
            result = (source_type_status, source_type_data)
        
        return result
    
    def _get_source_type_by_id(self, request):

        source_type_id = request.GET.get('source_type_id')
        source_type_status, source_type_data = self._service_helper.get_by_id(source_type_id, InformationSourceType)

        if source_type_status:
            result = (source_type_status, InformationSourceTypeSerializer(source_type_data).data)
        
        else:
            result = (source_type_status, source_type_data)
        
        return result
    
    def _get_all_activity(self, request):

        activity_status, activity_data = self._service_helper.get_all(Activity)

        if activity_status:
            result = (activity_status, ActivitySerializer(activity_data, many=True).data)
        
        else:
            result = (activity_status, activity_data)
        
        return result
    
    def _get_activity_by_id(self, request):

        activity_id = request.GET.get('activity_id')
        activity_status, activity_data = self._service_helper.get_by_id(activity_id, Activity)

        if activity_status:
            result = (activity_status, ActivitySerializer(activity_data).data)
        
        else:
            result = (activity_status, activity_data)
        
        return result
    
    def _get_all_information_source_type(self, request):

        information_source_type_status, information_source_type_data = self._service_helper.get_all(InformationSourceType)

        if information_source_type_status:
            result = (information_source_type_status, InformationSourceTypeSerializer(information_source_type_data, many=True).data)
        
        else:
            result = (information_source_type_status, information_source_type_data)
        
        return result
    
    def _get_information_source_type_by_id(self, request):

        information_source_type_id = request.GET.get('information_source_type_id')
        information_source_type_status, information_source_type_data = self._service_helper.get_by_id(information_source_type_id, InformationSourceType)

        if information_source_type_status:
            result = (information_source_type_status, InformationSourceTypeSerializer(information_source_type_data).data)
        
        else:
            result = (information_source_type_status, information_source_type_data)
        
        return result

    def _get_all_general_impact(self, request):

        general_impact_status, general_impact_data = self._service_helper.get_all(GeneralImpact)

        if general_impact_status:
            result = (general_impact_status, GeneralImpactSerializer(general_impact_data, many=True).data)
        
        else:
            result = (general_impact_status, general_impact_data)
        
        return result
    
    def _get_general_impact_by_id(self, request):

        general_impact_id = request.GET.get('general_impact_id')
        general_impact_status, general_impact_data = self._service_helper.get_by_id(general_impact_id, GeneralImpact)

        if general_impact_status:
            result = (general_impact_status, GeneralImpactSerializer(general_impact_data).data)
        
        else:
            result = (general_impact_status, general_impact_data)
        
        return result

    def _get_all_classifier(self, request):

        classifier_status, classifier_data = self._service_helper.get_all(Classifier)

        if classifier_status:
            result = (classifier_status, ClassifierSerializer(classifier_data, many=True).data)
        
        else:
            result = (classifier_status, classifier_data)
        
        return result

    def _get_classifier_by_id(self, request):
    
        classifier_id = request.GET.get('classifier_id')
        classifier_status, classifier_data = self._service_helper.get_by_id(classifier_id, Classifier)

        if classifier_status:
            result = (classifier_status, ClassifierSerializer(classifier_data).data)
        
        else:
            result = (classifier_status, classifier_data)
        
        return result

    def _get_all_temporality_impact(self, request):

        temporality_impact_status, temporality_impact_data = self._service_helper.get_all(TemporalityImpact)

        if temporality_impact_status:
            result = (temporality_impact_status, TemporalityImpactSerializer(temporality_impact_data, many=True).data)
        
        else:
            result = (temporality_impact_status, temporality_impact_data)
        
        return result

    def _get_temporality_impact_by_id(self, request):

        temporality_impact_id = request.GET.get('temporality_impact_id')
        temporality_impact_status, temporality_impact_data = self._service_helper.get_by_id(temporality_impact_id, TemporalityImpact)

        if temporality_impact_status:
            result = (temporality_impact_status, TemporalityImpactSerializer(temporality_impact_data).data)
        
        else:
            result = (temporality_impact_status, temporality_impact_data)
        
        return result

    ## auxiliar function
    def _increase_review_counter(self, mitigation_action):
        mitigation_action.review_count += 1
        mitigation_action.save()
    
    
    def _update_fsm_state(self, next_state, adaptation_action, user):

        result = (False, self.INVALID_STATUS_TRANSITION)
        # --- Transition ---
        # source -> target

        transitions = adaptation_action.get_available_fsm_state_transitions()
        states = {}
        for transition in  transitions:
            states[transition.target] = transition

        states_keys = states.keys()
        if len(states_keys) <= 0: result = (False, self.STATE_HAS_NO_AVAILABLE_TRANSITIONS)

        if next_state in states_keys:
            state_transition= states[next_state]
            transition_function = getattr(adaptation_action ,state_transition.method.__name__)
            previous_state = adaptation_action.fsm_state

            if has_transition_perm(transition_function, user):
                transition_function()
                adaptation_action.save()
                
                ##change_log_data = self._serialize_change_log_data(user, adaptation_action, previous_state)
                ##serialized_change_log = self._get_serialized_change_log(change_log_data)
                ##if serialized_change_log.is_valid():
                ##serialized_change_log.save()
                result = (True, adaptation_action)

                ##else:
                ##    result = (False, serialized_change_log.errors)

            else: result = (False, self.INVALID_USER_TRANSITION)

        return result
    
    
    def get(self, request, adaptation_action_id):
        
        adaptation_action_status, adaptation_action_data = self._service_helper.get_one(AdaptationAction, adaptation_action_id)
        
        if adaptation_action_status:
            result = (adaptation_action_status, AdaptationActionSerializer(adaptation_action_data).data)
        
        else:
            result = (adaptation_action_status, adaptation_action_data) 

        return result
    
    def get_all(self, request):

        adaptation_action_status, adaptation_action_data = self._service_helper.get_all(AdaptationAction)

        if adaptation_action_status:
            result = (adaptation_action_status, AdaptationActionSerializer(adaptation_action_data, many=True).data)
        
        else:
            result = (adaptation_action_status, adaptation_action_data) 

        return result


    def create(self, request):

        errors =[]
        validation_dict = {}
        data = request.data.copy()
        data['user'] = request.user.id

        # fk's of object adaptation_action that have nested fields
        field_list = ['report_organization', 'address', 'adaptation_action_information', 'activity', 'instrument', 'climate_threat', 'implementation', 'finance',
            'status', 'source', 'finance_instrument', 'mideplan', 'indicator', 'progress_log', 'indicator_monitoring', 'general_report', 'action_impact']

        for field in field_list:
            if data.get(field, False):
                record_status, record_data = self._create_sub_record(data.get(field), field)
                
                if record_status:
                    data[field] = record_data.id
                dict_data = record_data if isinstance(record_data, list) else [record_data]
                validation_dict.setdefault(record_status,[]).extend(dict_data)
        
        if all(validation_dict):
            serialized_adaptation_action = self._get_serialized_adaptation_action(data)
            if serialized_adaptation_action.is_valid():
                adaptation_action = serialized_adaptation_action.save()
                
                result = (True, AdaptationActionSerializer(adaptation_action).data)
  
            else:
                errors.append(serialized_adaptation_action.errors)
                result = (False, errors)
        else:
            result = (False, validation_dict.get(False))
            
        return result
    
    def update(self, request, adaptation_action_id):

        validation_dict = {}
        data = request.data.copy()
        data['user'] = request.user.id

        field_list = ['report_organization', 'address', 'adaptation_action_information', 'activity', 'instrument', 'climate_threat', 'implementation', 'finance',
            'status', 'source', 'finance_instrument', 'mideplan', 'indicator', 'progress_log', 'indicator_monitoring', 'general_report', 'action_impact']
        adaptation_action_status, adaptation_action_data = \
            self._service_helper.get_one(AdaptationAction, adaptation_action_id)
        
        if adaptation_action_status:
            adaptation_action = adaptation_action_data
             # fk's of object adaptation that have nested fields
            for field in field_list:
                if data.get(field, False):
                    record_status, record_data = self._create_or_update_record(adaptation_action, field, data.get(field))
                    
                    if record_status:
                        data[field] = record_data.id
                        
                    dict_data = record_data if isinstance(record_data, list) else [record_data]
                    validation_dict.setdefault(record_status,[]).extend(dict_data)

            if all(validation_dict):
                serialized_adaptation_action = self._get_serialized_adaptation_action(data, adaptation_action)
                
                if serialized_adaptation_action.is_valid():
                    adaptation_action = serialized_adaptation_action.save()
                    result = (True, AdaptationActionSerializer(adaptation_action).data)

                else:
                    result = (False, serialized_adaptation_action.errors)
            else:
                result = (False, validation_dict.get(False))
        else:
            result = (adaptation_action_status, adaptation_action_data)


        return result
    
    
    def patch(self, request, adaptation_action_id):
        ## missing review and comments here!!
        data = request.data
        next_state, user = data.pop('fsm_state', None), request.user
        comment_list = data.pop('comments', [])

        adaptation_action_status, adaptation_action_data = \
            self._service_helper.get_one(AdaptationAction, adaptation_action_id)

        if adaptation_action_status:
            adaptation_action = adaptation_action_data
            if next_state:
                update_status, update_data = self._update_fsm_state(next_state, adaptation_action, user)
                if update_status:
                    self._increase_review_counter(adaptation_action)
                    ##assign_status, assign_data = self._assign_comment(comment_list, adaptation_action, user)

                    ##if assign_status: 
                    result = (True, AdaptationActionSerializer(adaptation_action).data)
                    ##else: result = (assign_status, assign_data)
                
                else:
                    result = (update_status, update_data)
            else:
                result = (False, self.INVALID_STATUS_TRANSITION)
        else:
            result = (adaptation_action_status, adaptation_action_data)
        
        return result