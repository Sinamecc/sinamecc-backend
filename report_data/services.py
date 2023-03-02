from general.storages import S3Storage
from mitigation_action.models import Classifier, InformationSourceType, ThematicCategorizationType
from report_data.models import ReportData, ReportFile
from general.helpers.services import ServiceHelper
from general.helpers.serializer import SerializersHelper
from report_data.serializers import ChangeLogSerializer, ReportDataSerializer, ReportDataChangeLogSerializer, ReportFileSerializer
from mitigation_action.serializers import ClassifierSerializer, ContactSerializer, InformationSourceTypeSerializer, ThematicCategorizationTypeSerializer
from workflow.serializers import CommentSerializer
from workflow.services import WorkflowService
import os
from django_fsm import has_transition_perm
from io import BytesIO
from rolepermissions.checkers import has_role, has_object_permission

# TODO: Add exception handling
class ReportDataService():
    def __init__(self):
        self._service_helper = ServiceHelper(self)
        self._serializer_helper = SerializersHelper()
        self._workflow_service = WorkflowService()
        self._storage = S3Storage()
        self.FUNCTION_INSTANCE_ERROR = 'Error Mitigation Action Service does not have {0} function'
        self.ATTRIBUTE_INSTANCE_ERROR = 'Instance Model does not have {0} attribute'
        self.INVALID_STATUS_TRANSITION = "Invalid report data state transition."
        self.STATE_HAS_NO_AVAILABLE_TRANSITIONS = "State has no available transitions."
        self.ACCESS_DENIED_ALL = "Access denied to all report data"
        self.ACCESS_DENIED = "Access denied to report data: {0}"


    def _get_serialized_report_data(self,  data, report_data=None, partial=None):

        serializer = self._serializer_helper.get_serialized_record(ReportDataSerializer, data, record=report_data, partial=partial)

        return serializer
    

    def _get_serialized_report_data_change_log(self, data, report_data_change_log=None, partial=None):

        serializer = self._serializer_helper.get_serialized_record(ReportDataChangeLogSerializer, data, record=report_data_change_log, partial=partial)

        return serializer


    def _get_serialized_contact(self,  data, contact=None, partial=None):
        
        serializer = self._serializer_helper.get_serialized_record(ContactSerializer, data, record=contact, partial=partial)

        return serializer


    def _get_report_data_change_log_data(self, data, user):

        data = {
            'author': user.id,
            'changes': data.get('changes', None),
            'change_description': data.get('change_description', None),
        }

        return data
    
    def _get_report_file_data(self, data, file):
        
        data = {
            'file': file,
            'filename': file.name,
            'report_data': data.get('report_data', None),
            'report_type': data.get('report_type', None),
        }

        return data


    def _get_serialized_change_log(self, data, change_log=False, partial=False):
    
        serializer = self._serializer_helper.get_serialized_record(ChangeLogSerializer, data, record=change_log, partial=partial)

        return serializer
    
    
    def _serialize_change_log_data(self, user, report_data, previous_status):

        data = {
            'report_data': report_data.id,
            'user': user.id,
            'current_status': report_data.fsm_state,
            'previous_status': previous_status
        }

        return data
    
    def _create_update_contact(self, data, contact=None):
        
        if contact:
            serialized_contact = self._get_serialized_contact(data, contact)

        else:
            serialized_contact = self._get_serialized_contact(data)
        
        if serialized_contact.is_valid():
            contact = serialized_contact.save()
            result = (True, contact)

        else:
            result = (False, serialized_contact.errors)

        return result


    def _create_update_report_data_change_log(self, data, report_data_change_log=None):
            
        if report_data_change_log:
            serialized_report_data_change_log = self._get_serialized_report_data_change_log(data, report_data_change_log)

        else:
            serialized_report_data_change_log = self._get_serialized_report_data_change_log(data)
        
        if serialized_report_data_change_log.is_valid():
            report_data_change_log = serialized_report_data_change_log.save()
            result = (True, report_data_change_log)

        else:
            result = (False, serialized_report_data_change_log.errors)

        return result

    ## aux function
        ## auxiliar function
    def _increase_review_counter(self, report_data):
        report_data.review_count += 1
        report_data.save()


    def _assign_comment(self, comment_list, report_data, user):

        data = [{**comment, 'fsm_state': report_data.fsm_state, 'user': user.id, 'review_number': report_data.review_count}  for comment in comment_list]
        comment_list_status, comment_list_data = self._workflow_service.create_comment_list(data)

        if comment_list_status:
            report_data.comments.add(*comment_list_data)
            result = (True, comment_list_data)

        else:
            result = (False, comment_list_data)

        return result

    
    def _update_fsm_state(self, next_state, report_data, user):

        result = (False, self.INVALID_STATUS_TRANSITION)
        # --- Transition ---
        # source -> target

        transitions = report_data.get_available_fsm_state_transitions()
        states = {}
        for transition in  transitions:
            states[transition.target] = transition

        states_keys = states.keys()
        if len(states_keys) <= 0: result = (False, self.STATE_HAS_NO_AVAILABLE_TRANSITIONS)

        if next_state in states_keys:
            state_transition= states[next_state]
            transition_function = getattr(report_data ,state_transition.method.__name__)
            previous_state = report_data.fsm_state

            if has_transition_perm(transition_function, user):
                transition_function(user)
                report_data.save()
                
                change_log_data = self._serialize_change_log_data(user, report_data, previous_state)
                serialized_change_log = self._get_serialized_change_log(change_log_data)
                if serialized_change_log.is_valid():
                    serialized_change_log.save()
                    result = (True, report_data)

                else:
                    result = (False, serialized_change_log.errors)

            else: result = (False, self.INVALID_USER_TRANSITION)

        return result
    
    
    def get(self, request, report_data_id):
        
        report_data_status, report_data_details = self._service_helper.get_one(ReportData, report_data_id)
        if not report_data_status:
            result = (report_data_status, report_data_details)
        
        elif not has_object_permission('access_report_data_register', request.user, report_data_details):
            result = (False, self.ACCESS_DENIED.format(report_data_details.id))
        
        elif report_data_status:
            result = (report_data_status, ReportDataSerializer(report_data_details).data)

        return result

    
    def get_all(self, request):
        user =  request.user
        report_data_status, report_data_details = None, None
        
        if has_role(user,['reviewer', 'reviewer_report_data', 'admin']):
            report_data_status, report_data_details = self._service_helper.get_all(ReportData)
            
        elif has_role(user, ['information_provider_report_data', 'information_provider']):
            report_data_status, report_data_details = \
                self._service_helper.get_all(ReportData, user=user)
        else:
            return (False, self.ACCESS_DENIED_ALL)
        
        if report_data_status:
            result = (True, ReportDataSerializer(report_data_details, many=True).data)

        else:
            result = (False, report_data_details)

        return result


    def create(self, request):

        validation_dict, errors = {}, []
        data = request.data.copy()
        data['user'] = request.user.id
        data['report_data_change_log'] = self._get_report_data_change_log_data(data.get('report_data_change_log', {}), request.user)
        field_list = ['contact']

        validation_dict = self._service_helper.create_or_update_record(field_list, data)

        if all(validation_dict):
            is_complete = data.pop('is_complete', False)
            serialized_report_data_change_log = self._get_serialized_report_data_change_log(data.pop('report_data_change_log'), partial=True)
            serialized_report_data = self._get_serialized_report_data(data, partial=True)
            
            if all([serialized_report_data.is_valid(), serialized_report_data_change_log.is_valid()]):

                report_data = serialized_report_data.save()

                if is_complete:
                        report_data.submit(request.user)
                        report_data.save()

                report_data_change_log = serialized_report_data_change_log.save()
                report_data.report_data_change_log.add(report_data_change_log)
                result = (True, ReportDataSerializer(report_data).data)
  
            else:
                
                errors.append({**serialized_report_data.errors ,**serialized_report_data_change_log.errors})
                result = (False, errors)
        else:
            result = (False, validation_dict.get(False))
            
        return result
    

    def update(self, request, report_data_id):

        validation_dict, errors = {}, []
        data = request.data.copy()
        data['report_data_change_log'] = self._get_report_data_change_log_data(data.get('report_data_change_log', {}), request.user)

        field_list = ['contact']
        report_data_status, report_data_details = self._service_helper.get_one(ReportData, report_data_id)
        if not has_object_permission('access_report_data_register', request.user, report_data_details):
            return (False, self.ACCESS_DENIED.format(report_data_details.id))
        
        if report_data_status:
            validation_dict = self._service_helper.create_or_update_record(field_list, data, report_data_details)

            if all(validation_dict):
                is_complete = data.pop('is_complete', False)
                serialized_report_data_change_log = self._get_serialized_report_data_change_log(data.pop('report_data_change_log'), partial=True)
                serialized_report_data = self._get_serialized_report_data(data, report_data=report_data_details, partial=True)

                if serialized_report_data.is_valid() and serialized_report_data_change_log.is_valid():
                    report_data = serialized_report_data.save()

                    if is_complete:
                        report_data.submit(request.user)
                        report_data.save()
                        
                    report_data_change_log = serialized_report_data_change_log.save()
                    report_data.report_data_change_log.add(report_data_change_log)
                    
                    result = (True, ReportDataSerializer(report_data).data)
    
                else:
                    errors.append(serialized_report_data.errors)
                    result = (False, errors)

            else:
                result = (False, validation_dict.get(False))

        else:
            result = (False, report_data_details)
            
        return result

    
    def upload_report_file(self, file, report_data, type=None):
        data = {'report_data': report_data.id, 'report_type': type}
        data = self._get_report_file_data(data, file)
        report_file = report_data.report_file.filter(report_type=type).first()
        serialized_report_file = ReportFileSerializer(report_file, data=data, partial=True)
        
        if serialized_report_file.is_valid():
            saved_report_file = serialized_report_file.save()
            result = (True, ReportFileSerializer(saved_report_file).data)
            
        else:
            result = (False, serialized_report_file.errors)
            
        return result
        

    ## upload files in the models
    def upload_file_to(self, request, report_data_id):

        files_type = {
            'report_file': self.upload_report_file,
            'base_line_report': self.upload_report_file
        }
        
        data = request.data
        
        report_status, report_data = self._service_helper.get_one(ReportData, report_data_id)
        
        status_upload_files = {}
        if report_status:
            
            for k, v in data.items():
                
                if k in files_type:
                    result_status, result_data = files_type.get(k)(v, report_data, k)
                    status_upload_files.setdefault(result_status, []).append(result_data)
            
            if all(status_upload_files) and  status_upload_files:
                files_list = status_upload_files.get(True)
                result = (True, ReportDataSerializer(report_data).data)
            
            else:
                error_list = status_upload_files.get(False)
                result = (False, error_list)
            
            
        else:
            
            result = (report_status, report_data)
       
        
        return result
    
    
    def delete(self, request, report_data_id):
        
        report_data_status, report_data_details = self._service_helper.get_one(ReportData, report_data_id)
        if not has_object_permission('access_report_data_register', request.user, report_data_details):
            return (False, self.ACCESS_DENIED.format(report_data_details.id))

        if report_data_status:
            serialized_report_data = ReportDataSerializer(report_data_details).data
            report_data_details.delete()
            result = (True, serialized_report_data)
        
        else: 
            result = (report_data_status, report_data_details)
        
        return result
    
    def patch(self, request, report_data_id):

        data = request.data
        next_state, user = data.pop('fsm_state', None), request.user
        comment_list = data.pop('comments', [])

        report_data_status, report_data = \
            self._service_helper.get_one(ReportData, report_data_id)

        if report_data_status:
            if next_state:
                update_status, update_data = self._update_fsm_state(next_state, report_data, user)
                if update_status:
                    self._increase_review_counter(report_data)
                    assign_status, assign_data = self._assign_comment(comment_list, report_data, user)

                    if assign_status: 
                        result = (True, ReportDataSerializer(report_data).data)
                    
                    else: 
                        result = (assign_status, assign_data)
                
                else:
                    result = (update_status, update_data)
            else:
                result = (False, self.INVALID_STATUS_TRANSITION)
        else:
            result = (report_data_status, report_data)
        
        return result
    
    
    def _get_content_file(self, path):

        path, filename = os.path.split(path)
        
        result = (filename, BytesIO(self._storage.get_file(path)))
        
        return result
    
    
    def download_report_file(self, request, report_file_id):
        
        report_file_status, report_file_data = self._service_helper.get_one(ReportFile, report_file_id)
        
        if report_file_status:
            
            s3_path = report_file_data.file.name
            
            path, filename = os.path.split(s3_path)
        
            file_content =  BytesIO(self._storage.get_file(s3_path))
            result = (True, (filename, file_content))
            
        else:
            result = (report_file_status, report_file_data)

        return result
    
    
    def download_source_file(self, request, report_data_id):
        
        report_data_status, report_data = self._service_helper.get_one(ReportData, report_data_id)
        
        if report_data_status:
            s3_path = report_data.source_file.name
            
            path, filename = os.path.split(s3_path)
        
            file_content =  BytesIO(self._storage.get_file(s3_path))
            
            result = (True, (filename, file_content))
            
        else:
            result = (report_data_status, report_data)

        return result
    
    
    def get_catalog_data(self, request):
    
        catalog = {
            'classifier': (Classifier, ClassifierSerializer),
            'thematic_categorization_type': (ThematicCategorizationType, ThematicCategorizationTypeSerializer),
            'information_source_type': (InformationSourceType, InformationSourceTypeSerializer),
        }
        data = {}
        for name , (_model, _serializer) in catalog.items():
            result_status, result_data = self._service_helper.get_all(_model)

            if not result_status:
                result = (False, result_data)
                return result
            
            data = {**data, **{name: _serializer(result_data, many=True).data}}
        
        result = (True, data)
        
        return result
    
    
    def get_current_comments(self, request, report_data_id):

        report_data_status, report_data = self._service_helper.get_one(ReportData, report_data_id)

        if report_data_status:
            review_number = report_data.review_count
            fsm_state = report_data.fsm_state
            comment_list = report_data.comments.filter(review_number=review_number, fsm_state=fsm_state).all()

            serialized_comment = CommentSerializer(comment_list, many=True)

            result = (True, serialized_comment.data)

        else:
            result = (report_data_status, report_data)

        return result


    def get_comments_by_fsm_state_or_review_number(self, request, report_data_id, fsm_state=None, review_number=None):
        
        report_data_status, report_data = self._service_helper.get_one(ReportData, report_data_id)
        search_key = lambda x, y: { x:y } if y else {}
        if report_data_status:

            search_kwargs = {**search_key('fsm_state', fsm_state), **search_key('review_number', review_number)}
            comment_list = report_data.comments.filter(**search_kwargs).all()

            serialized_comment = CommentSerializer(comment_list, many=True)

            result = (True, serialized_comment.data)

        else:
            result = (report_data_status, report_data)

        return result

