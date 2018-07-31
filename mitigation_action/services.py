from mitigation_action.models import RegistrationType, Institution, Contact, Status, ProgressIndicator, FinanceSourceType, Finance, IngeiCompliance, GeographicScale, Location, Mitigation, ChangeLog
from mitigation_action.serializers import FinanceSerializer, LocationSerializer, ProgressIndicatorSerializer, ContactSerializer, MitigationSerializer, ChangeLogSerializer
from workflow.models import ReviewStatus
from general.storages import S3Storage
from rest_framework.parsers import JSONParser
import datetime
import uuid

from workflow.services import WorkflowService
workflow_service = WorkflowService()

class MitigationActionService():
    def __init__(self):
        self.storage = S3Storage()
        self.MITIGATION_ACTION_DOES_NOT_EXIST = "Mitigation Action does not exist."
        self.MITIGATION_ACTION_ERROR_GET_ALL = "Error retrieving all Mitigation Action records."
        self.INGEI_COMPLIANCE_DOES_NOT_EXIST = "INGEI compliance does not exist."
        self.COMMENT_NOT_ASSIGNED = "The provided comment could not be assigned correctly."
        self.NO_PATCH_DATA_PROVIDED = "No PATCH data provided."
        self.CHANGE_LOG_DOES_NOT_EXIST = "Mitigation Action change log does not exist."

    def get_all(self, language):
        try:
            mitigations_list = [
                {
                    'id': m.id,
                    'strategy_name': m.strategy_name,
                    'name': m.name,
                    'purpose': m.purpose,
                    'quantitative_purpose': m.quantitative_purpose,
                    'start_date': m.start_date,
                    'end_date': m.end_date,
                    'gas_inventory': m.gas_inventory,
                    'emissions_source': m.emissions_source,
                    'carbon_sinks': m.carbon_sinks,
                    'impact_plan': m.impact_plan,
                    'impact': m.impact,
                    'bibliographic_sources': m.bibliographic_sources,
                    'is_international': m.is_international,
                    'international_participation': m.international_participation,
                    'sustainability': m.sustainability,
                    'question_ucc': m.question_ucc,
                    'question_ovv': m.question_ovv,
                    'user': {
                        'id': m.user.id,
                        'username': m.user.username,
                        'email': m.user.email
                    },
                    'registration_type': {
                        'id': m.registration_type.id,
                        'type': m.registration_type.type_es if language=="es" else m.registration_type.type_en,
                    },
                    'institution': {
                        'id': m.institution.id,
                        'name': m.institution.name
                    },
                    'contact': {
                        'id': m.contact.id,
                        'full_name': m.contact.full_name,
                        'job_title': m.contact.job_title,
                        'email': m.contact.email,
                        'phone': m.contact.phone
                    },
                    'status': {
                        'id': m.status.id,
                        'status': m.status.status_es if language=="es" else m.status.status_en
                    },
                    'progress_indicator': {
                        'id': m.progress_indicator.id,
                        'name': m.progress_indicator.name,
                        'type': m.progress_indicator.type,
                        'unit': m.progress_indicator.unit,
                        'start_date': m.progress_indicator.start_date
                    },
                    'finance': {
                        'id': m.finance.id,
                        'finance_source_type': {
                            'id': m.finance.finance_source_type.id,
                            'name': m.finance.finance_source_type.name_es if language=="es" else m.finance.finance_source_type.name_en
                        },
                        'source': m.finance.source
                    },
                    'ingei_compliances': [
                        {
                            'id': ingei.id,
                            'name': ingei.name_es if language=="es" else ingei.name_en,
                        } for ingei in m.ingei_compliances.all()
                    ],
                    'geographic_scale': {
                        'id': m.geographic_scale.id,
                        'name': m.geographic_scale.name_es if language=="es" else m.geographic_scale.name_en
                    },
                    'location': {
                        'id': m.location.id,
                        'geographical_site': m.location.geographical_site,
                        'is_gis_annexed': m.location.is_gis_annexed
                    },
                    # Workflow
                    'review_status': {
                        'id': m.review_status.id,
                        'status': m.review_status.status
                    },
                    'review_count': m.review_count,
                    'comments': [
                        {
                            'id': comment.id,
                            'comment': comment.comment
                        } for comment in m.comments.all()
                    ],
                    'created': m.created,
                    'updated': m.updated 
                } for m in Mitigation.objects.all()
            ]
            result = (True, mitigations_list)
        except Mitigation.DoesNotExist:
            result (False, self.MITIGATION_ACTION_ERROR_GET_ALL)
        return result

    def get_serialized_contact(self, request):
        contact_data = {
            'full_name': request.data.get('contact[full_name]'),
            'job_title': request.data.get('contact[job_title]'),
            'email': request.data.get('contact[email]'),
            'phone': request.data.get('contact[phone]'),
        }
        serializer = ContactSerializer(data=contact_data)
        return serializer

    def get_serialized_contact_for_existing(self, request, contact):
        contact_data = {
            'full_name': request.data.get('contact[full_name]'),
            'job_title': request.data.get('contact[job_title]'),
            'email': request.data.get('contact[email]'),
            'phone': request.data.get('contact[phone]'),
        }
        serializer = ContactSerializer(contact, data=contact_data)
        return serializer

    def get_serialized_progress_indicator(self, request):
        progress_indicator_data = {
            'name': request.data.get('progress_indicator[name]'),
            'type': request.data.get('progress_indicator[type]'),
            'unit': request.data.get('progress_indicator[unit]'),
            'start_date': request.data.get('progress_indicator[start_date]')
        }
        serializer = ProgressIndicatorSerializer(data=progress_indicator_data)
        return serializer

    def get_serialized_progress_indicator_for_existing(self, request, progress_indicator):
        progress_indicator_data = {
            'name': request.data.get('progress_indicator[name]'),
            'type': request.data.get('progress_indicator[type]'),
            'unit': request.data.get('progress_indicator[unit]'),
            'start_date': request.data.get('progress_indicator[start_date]')
        }
        serializer = ProgressIndicatorSerializer(progress_indicator, data=progress_indicator_data)
        return serializer

    def get_serialized_location(self, request):
        location_data = {
            'geographical_site': request.data.get('location[geographical_site]'),
            'is_gis_annexed': request.data.get('location[is_gis_annexed]')
        }
        serializer = LocationSerializer(data=location_data)
        return serializer

    def get_serialized_location_for_existing(self, request, location):
        location_data = {
            'geographical_site': request.data.get('location[geographical_site]'),
            'is_gis_annexed': request.data.get('location[is_gis_annexed]')
        }
        serializer = LocationSerializer(location, data=location_data)
        return serializer

    def get_serialized_finance(self, request):
        finance_data = {
            'finance_source_type': request.data.get('finance[finance_source_type]'),
            'source': request.data.get('finance[source]'),
        }
        serializer = FinanceSerializer(data=finance_data)
        return serializer

    def get_serialized_finance_for_existing(self, request, finance):
        finance_data = {
            'finance_source_type': request.data.get('finance[finance_source_type]'),
            'source': request.data.get('finance[source]'),
        }
        serializer = FinanceSerializer(finance, data=finance_data)
        return serializer

    def get_review_status_id(self, status):
        review_status_id_result, review_status_id_data = workflow_service.get_review_status_id(status)
        return review_status_id_data

    def get_review_count(self, review_status_id, current_count):
        in_review_status_id = self.get_review_status_id(workflow_service.IN_REVIEW_STATUS)
        if review_status_id == in_review_status_id:
            current_count += 1
        return current_count

    def get_serialized_mitigation_action(self, request, contact_id, progress_indicator_id, location_id, finance_id):
        mitigation_data = {
            'id': str(uuid.uuid4()),
            'strategy_name': request.data.get('strategy_name'),
            'name': request.data.get('name'),
            'purpose': request.data.get('purpose'),
            'quantitative_purpose': request.data.get('quantitative_purpose'),
            'start_date': request.data.get('start_date'),
            'end_date': request.data.get('end_date'),
            'gas_inventory': request.data.get('gas_inventory'),
            'emissions_source': request.data.get('emissions_source'),
            'carbon_sinks': request.data.get('carbon_sinks'),
            'impact_plan': request.data.get('impact_plan'),
            'impact': request.data.get('impact'),
            'bibliographic_sources': request.data.get('bibliographic_sources'),
            'is_international': request.data.get('is_international'),
            'international_participation': request.data.get('international_participation'),
            'sustainability': request.data.get('sustainability'),
            'question_ucc': request.data.get('question_ucc'),
            'question_ovv': request.data.get('question_ovv'),
            'user': request.data.get('user'),
            'registration_type': request.data.get('registration_type'),
            'institution': request.data.get('institution'),
            'contact': contact_id,
            'status': request.data.get('status'),
            'progress_indicator': progress_indicator_id,
            'finance': finance_id,
            'geographic_scale': request.data.get('geographic_scale'),
            'location': location_id,
            # Workflow
            'review_count': 0, # By default when creating
            'review_status': self.get_review_status_id(workflow_service.SUBMITTED_STATUS)
        }
        serializer = MitigationSerializer(data=mitigation_data)
        return serializer

    def get_serialized_mitigation_action_for_existing(self, request, mitigation, contact_id, progress_indicator_id, location_id, finance_id, review_count):
        mitigation_data = {
            'id': str(uuid.uuid4()),
            'strategy_name': request.data.get('strategy_name'),
            'name': request.data.get('name'),
            'purpose': request.data.get('purpose'),
            'quantitative_purpose': request.data.get('quantitative_purpose'),
            'start_date': request.data.get('start_date'),
            'end_date': request.data.get('end_date'),
            'gas_inventory': request.data.get('gas_inventory'),
            'emissions_source': request.data.get('emissions_source'),
            'carbon_sinks': request.data.get('carbon_sinks'),
            'impact_plan': request.data.get('impact_plan'),
            'impact': request.data.get('impact'),
            'bibliographic_sources': request.data.get('bibliographic_sources'),
            'is_international': request.data.get('is_international'),
            'international_participation': request.data.get('international_participation'),
            'sustainability': request.data.get('sustainability'),
            'question_ucc': request.data.get('question_ucc'),
            'question_ovv': request.data.get('question_ovv'),
            'user': request.data.get('user'),
            'registration_type': request.data.get('registration_type'),
            'institution': request.data.get('institution'),
            'contact': contact_id,
            'status': request.data.get('status'),
            'progress_indicator': progress_indicator_id,
            'finance': finance_id,
            'geographic_scale': request.data.get('geographic_scale'),
            'location': location_id,
            'review_count': mitigation.review_count,
            'review_status': mitigation.review_status.id
        }
        serializer = MitigationSerializer(mitigation, data=mitigation_data)
        return serializer

    def assign_ingei_compliances(self, request, mitigation_action):
        ingei_ids_str = request.data.get('ingei_compliances')
        ingei_ids_array = list(map(int, ingei_ids_str.split(',')))
        for id in ingei_ids_array:
            try:
                ingei = IngeiCompliance.objects.get(pk=id)
                mitigation_action.ingei_compliances.add(ingei)
                result = (True, mitigation_action)
            except IngeiCompliance.DoesNotExist:
                result = (False, self.INGEI_COMPLIANCE_DOES_NOT_EXIST)
        return result

    def assign_comment(self, request, mitigation_action):
        comment_result_status, comment_result_data = workflow_service.create_comment(request)
        if comment_result_status:
            comment = comment_result_data
            mitigation_action.comments.add(comment)
        return comment_result_status

    def get_serialized_change_log(self, mitigation_id, previous_status_id, current_status_id, user):
        change_log_data = {
            'mitigation_action': mitigation_id,
            'previous_status': previous_status_id,
            'current_status': current_status_id,
            'user': user
        }
        serializer = ChangeLogSerializer(data=change_log_data)
        return serializer

    def create_change_log_entry(self, mitigation, previous_status, current_status, user):
        serialized_change_log = self.get_serialized_change_log(mitigation.id, previous_status, current_status, user)
        if serialized_change_log.is_valid():
            serialized_change_log.save()
            result = (True, serialized_change_log.data)
        else:
            result = (False, serialized_change_log.errors)
        return result


    def getReviewStatus(self, id):
        return ReviewStatus.objects.get(pk=id)

    def get_change_log(self, id):
        try:
            mitigation = self.get_one(id)
            change_log_content = []
            for log in ChangeLog.objects.filter(mitigation_action=mitigation.id):
                previous_status = self.getReviewStatus(log.previous_status.id) if log.previous_status else None
                if previous_status:
                    previous_status_data = {
                        'id': previous_status.id,
                        'status': previous_status.status
                    }
                else:
                    previous_status_data = None
                current_status = self.getReviewStatus(log.current_status.id)
                current_status_data = {
                    'id': current_status.id,
                    'status': current_status.status
                }
                change_log_data = {
                    'date': log.date,
                    'mitigation_action': log.mitigation_action.id,
                    'previous_status': previous_status_data,
                    'current_status': current_status_data,
                    'user': log.user.id
                }
                change_log_content.append(change_log_data)
            result = (True, change_log_content)
        except Mitigation.DoesNotExist:
            result = (False, self.MITIGATION_ACTION_DOES_NOT_EXIST)
        return result

    def create(self, request):
        errors = []
        serialized_contact = self.get_serialized_contact(request)
        serialized_progress_indicator = self.get_serialized_progress_indicator(request)
        serialized_location = self.get_serialized_location(request)
        serialized_finance = self.get_serialized_finance(request)  
        valid_relations = serialized_contact.is_valid() and serialized_progress_indicator.is_valid() and serialized_location.is_valid() and serialized_finance.is_valid()
        if valid_relations:
            contact = serialized_contact.save()
            progress_indicator = serialized_progress_indicator.save()
            location = serialized_location.save()
            finance = serialized_finance.save()
            serialized_mitigation_action = self.get_serialized_mitigation_action(request, contact.id, progress_indicator.id, location.id, finance.id)

            if serialized_mitigation_action.is_valid():
                mitigation_previous_status = None
                mitigation_action = serialized_mitigation_action.save()
                self.create_change_log_entry(mitigation_action, mitigation_previous_status, self.get_review_status_id(workflow_service.SUBMITTED_STATUS), request.data.get('user'))
                get_ingei_result, data_ingei_result = self.assign_ingei_compliances(request, mitigation_action)
                if get_ingei_result:
                    result = (True, MitigationSerializer(mitigation_action).data)
                else:
                    errors.append(data_ingei_result)
                    result = (False, errors)
            else:
                errors.append(serialized_mitigation_action.errors)
                result = (False, errors)
        else:
            errors.append(serialized_contact.errors)
            errors.append(serialized_progress_indicator.errors)
            errors.append(serialized_location.errors)
            errors.append(serialized_finance.errors)
            result = (False, errors)
        return result

    def get_one(self, str_uuid):
        f_uuid = uuid.UUID(str_uuid)
        return Mitigation.objects.get(pk=f_uuid)


    def get(self, id, language):

        try:
            mitigation = self.get_one(id)
            content = {
                'id': mitigation.id,
                'strategy_name': mitigation.strategy_name,
                'name': mitigation.name,
                'purpose': mitigation.purpose,
                'quantitative_purpose': mitigation.quantitative_purpose,
                'start_date': mitigation.start_date,
                'end_date': mitigation.end_date,
                'gas_inventory': mitigation.gas_inventory,
                'emissions_source': mitigation.emissions_source,
                'carbon_sinks': mitigation.carbon_sinks,
                'impact_plan': mitigation.impact_plan,
                'impact': mitigation.impact,
                'bibliographic_sources': mitigation.bibliographic_sources,
                'is_international': mitigation.is_international,
                'international_participation': mitigation.international_participation,
                'sustainability': mitigation.sustainability,
                'question_ucc': mitigation.question_ucc,
                'question_ovv': mitigation.question_ovv,
                'user': {
                    'id': mitigation.user.id,
                    'username': mitigation.user.username,
                    'email': mitigation.user.email
                },
                'registration_type': {
                    'id': mitigation.registration_type.id,
                    'type': mitigation.registration_type.type_es if language=="es" else mitigation.registration_type.type_en,
                },
                'institution': {
                    'id': mitigation.institution.id,
                    'name': mitigation.institution.name
                },
                'contact': {
                    'id': mitigation.contact.id,
                    'full_name': mitigation.contact.full_name,
                    'job_title': mitigation.contact.job_title,
                    'email': mitigation.contact.email,
                    'phone': mitigation.contact.phone
                },
                'status': {
                    'id': mitigation.status.id,
                    'status': mitigation.status.status_es if language=="es" else mitigation.status.status_en
                },
                'progress_indicator': {
                    'id': mitigation.progress_indicator.id,
                    'name': mitigation.progress_indicator.name,
                    'type': mitigation.progress_indicator.type,
                    'unit': mitigation.progress_indicator.unit,
                    'start_date': mitigation.progress_indicator.start_date
                },
                'finance': {
                    'id': mitigation.finance.id,
                    'finance_source_type': {
                        'id': mitigation.finance.finance_source_type.id,
                        'name': mitigation.finance.finance_source_type.name_es if language=="es" else mitigation.finance.finance_source_type.name_en
                    },
                    'source': mitigation.finance.source
                },
                'ingei_compliances': [
                    {
                      'id': ingei.id,
                      'name': ingei.name_es if language=="es" else ingei.name_en
                    } for ingei in mitigation.ingei_compliances.all()
                ],
                'geographic_scale': {
                    'id': mitigation.geographic_scale.id,
                    'name': mitigation.geographic_scale.name_es if language=="es" else mitigation.geographic_scale.name_en
                },
                'location': {
                    'id': mitigation.location.id,
                    'geographical_site': mitigation.location.geographical_site,
                    'is_gis_annexed': mitigation.location.is_gis_annexed
                },
                # Workflow
                'review_status': {
                    'id': mitigation.review_status.id,
                    'status': mitigation.review_status.status
                },
                'review_count': mitigation.review_count,
                'comments': [
                    {
                        'id': comment.id,
                        'comment': comment.comment
                    } for comment in mitigation.comments.all()
                ],
                'created': mitigation.created,
                'updated': mitigation.updated
            }
            result = (True, content)
        except Mitigation.DoesNotExist:
            result = (False, self.MITIGATION_ACTION_DOES_NOT_EXIST)
        return result

    def delete(self, id):
        try:
            mitigation = self.get_one(id)
            mitigation.ingei_compliances.clear()
            mitigation.delete()
            result = True
        except:
            result = False
        return result

    def update(self, id, request):
        mitigation = self.get_one(id)
        contact_id = request.data.get('contact[id]')
        progress_indicator_id = request.data.get('progress_indicator[id]')
        location_id = request.data.get('location[id]')
        finance_id = request.data.get('finance[id]')
        contact = Contact.objects.get(pk=contact_id)
        progress_indicator = ProgressIndicator.objects.get(pk=progress_indicator_id)
        location = Location.objects.get(pk=location_id)
        finance = Finance.objects.get(pk=finance_id)
        serialized_contact = self.get_serialized_contact_for_existing(request, contact)
        serialized_progress_indicator = self.get_serialized_progress_indicator_for_existing(request, progress_indicator)
        serialized_location = self.get_serialized_finance_for_existing(request, location)
        serialized_finance = self.get_serialized_finance_for_existing(request, finance)
        valid_relations = serialized_contact.is_valid() and serialized_progress_indicator.is_valid() and serialized_location.is_valid() and serialized_finance.is_valid()
        if valid_relations:
            contact = serialized_contact.save()
            progress_indicator = serialized_progress_indicator.save()
            location = serialized_location.save()
            finance = serialized_finance.save()
            serialized_mitigation_action = self.get_serialized_mitigation_action_for_existing(request, mitigation, contact.id, progress_indicator.id, location.id, finance.id, mitigation.review_count)

            if serialized_mitigation_action.is_valid():
                mitigation_action = serialized_mitigation_action.save()
                mitigation.ingei_compliances.clear()
                get_ingei_result, data_ingei_result = self.assign_ingei_compliances(request, mitigation_action)
                if get_ingei_result:
                    result = (True, MitigationSerializer(mitigation_action).data)
                else:
                    errors.append(data_ingei_result)
                    result = (False, errors)
            else:
                errors.append(serialized_mitigation_action.errors)
                result = (False, errors)
        else:
            errors.append(serialized_contact.errors)
            errors.append(serialized_progress_indicator.errors)
            errors.append(serialized_location.errors)
            errors.append(serialized_finance.errors)
            result = (False, errors)
        return result

    def patch(self, id, request):
        mitigation = self.get_one(id)
        if (request.data.get('review_status')):
            patch_data = {
                'review_status': request.data.get('review_status'),
                'review_count': self.get_review_count(request.data.get('review_status'), mitigation.review_count)
            }
            serialized_mitigation_action = MitigationSerializer(mitigation, data=patch_data, partial=True)
            if serialized_mitigation_action.is_valid():
                mitigation_previous_status = mitigation.review_status.id
                mitigation_action = serialized_mitigation_action.save()
                self.create_change_log_entry(mitigation_action, mitigation_previous_status, mitigation_action.review_status.id, request.data.get('user'))
                result = (True, MitigationSerializer(mitigation_action).data)
            if (request.data.get('comment')):
                comment_status = self.assign_comment(request, mitigation_action)
                if comment_status:
                    result = (True, MitigationSerializer(mitigation_action).data)
                else:
                    result = (False, self.COMMENT_NOT_ASSIGNED)
        else:
            result = (False, self.NO_PATCH_DATA_PROVIDED)
        return result

    def get_form_data(self):       
        try:
            registration_types_list = [
                {
                    'id': rt.id,
                    'type_es': rt.type_es,
                    'type_en':rt.type_en
                } for rt in RegistrationType.objects.all()
            ]
            institutions_list = [
                {
                    'id': i.id,
                    'name': i.name
                } for i in Institution.objects.all()
            ]
            statuses_list = [
                {
                    'id': st.id,
                    'status_en': st.status_en,
                    'status_es': st.status_es
                } for st in Status.objects.all()
            ]
            finance_source_types_list = [
                {
                    'id': fst.id,
                    'name_es': fst.name_es,
                    'name_en': fst.name_en,
                } for fst in FinanceSourceType.objects.all()
            ]
            ingei_compliances_list = [
                {
                    'id': i.id,
                    'name_es': i.name_es,
                    'name_en': i.name_en,
                } for i in IngeiCompliance.objects.all()
            ]
            geographic_scales_list = [
                {
                    'id': g.id,
                    'name_es': g.name_es,
                    'name_en': g.name_en
                } for g in GeographicScale.objects.all()
            ]
            form_list = {
              'registration_types': registration_types_list,
              'institutions': institutions_list,
              'statuses': statuses_list,
              'finance_source_types': finance_source_types_list,
              'ingei_compliances': ingei_compliances_list,
              'geographic_scales': geographic_scales_list
            }
            result = (True, form_list)
        except Mitigation.DoesNotExist:
            result = (False, {'error': self.MITIGATION_ACTION_DOES_NOT_EXIST})
        return result

    # TODO Fix this multi-return method
    def get_form_data_es_en(self, language, option):
        Registration_Type = []

        if (option == "new" or option == "update"):
            Registration_Type.append(RegistrationType.objects.filter(type_key=option).get())
        else:
            return (False, {'error': "Parameter is not valid"})

        try:
            registration_types_list = [
                {
                    'id': rg.id,
                    'type': rg.type_es if language=="es" else rg.type_en
                } for rg in Registration_Type
            ]
            institutions_list = [
                {
                    'id': i.id,
                    'name': i.name 
                } for i in Institution.objects.all()
            ]
            statuses_list = [
                {
                    'id': st.id, 
                    'status': st.status_es if language=="es" else st.status_en
                  } for st in Status.objects.all()
            ]
            finance_source_types_list = [
                {
                    'id': fst.id,
                    'name': fst.name_es if language=="es" else fst.name_en
                } for fst in FinanceSourceType.objects.all()
            ]
            ingei_compliances_list = [
                {
                    'id': i.id,
                    'name': i.name_es if language=="es" else i.name_en
                } for i in IngeiCompliance.objects.all()
            ]
            geographic_scales_list = [
                {
                    'id': g.id,
                    'name': g.name_es if language=="es" else g.name_en 
                } for g in GeographicScale.objects.all()
            ]
            form_list = {
              'registration_types': registration_types_list,
              'institutions': institutions_list,
              'statuses': statuses_list,
              'finance_source_types': finance_source_types_list,
              'ingei_compliances': ingei_compliances_list,
              'geographic_scales': geographic_scales_list
            }
            result = (True, form_list)
        except Mitigation.DoesNotExist:
            result = (False, {'error': self.MITIGATION_ACTION_DOES_NOT_EXIST})
        return result