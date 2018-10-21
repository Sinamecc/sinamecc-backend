from django.urls import reverse
from general.storages import S3Storage
from mitigation_action.models import Mitigation
from mccr.models import MCCRRegistry, MCCRUserType, MCCRFile, OVV
from mccr.serializers import MCCRRegistrySerializerView, MCCRRegistrySerializerCreate, MCCRFileSerializer, MCCRRegistryOVVRelationSerializer
from rest_framework.parsers import JSONParser
from io import BytesIO
import uuid
import os
from django.contrib.auth.models import *

from general.services import EmailServices
email_sender  = "sinamec@grupoincocr.com" ##change to sinamecc email
ses_service = EmailServices(email_sender)
# TODO: Change is_valid() to exception
class MCCRService():
    def __init__(self):
        self.MCCR_ERROR_NOT_EXIST = "MCCR does not exists"
        self.MCCR_ERROR_GET_ALL = "Error retrieving all MCCR records"
        self.MCCR_ERROR_EMPTY_MITIGATIONS_LIST = "Empty mitigation actions list"
        self.MCCR_ERROR_EMPTY_OVV_LIST = "Empty OVV list"
        self.MCCR_ERROR_UNKNOWN_MITIGATION_LIST = "Unknown error retrieving mitigation actions list"

        self.storage = S3Storage()

    def get_serialized_mccr(self, request):
        d = {
            "status": request.data.get("status"),
            "user": request.user.id,
            "mitigation": request.data.get("mitigation"),
            "user_type": request.data.get("user_type")
        }
        serialized_mccr = MCCRRegistrySerializerCreate(data=d)
        return serialized_mccr

    def get_serialized_mccr_file(self, mccr_id, user_id, file):
        file_list = {
                "file": file,
                "user": user_id,
                "mccr": mccr_id
            }
        serializer = MCCRFileSerializer(data=file_list)
        return serializer

    def get_serialized_mccr_ovv_relation(self, mccr_id, ovv_id):
        mccr_ovv_relation = {"ovv": ovv_id, "mccr": mccr_id, "status": "ovv_assigned_first_review"}
        serializer = MCCRRegistryOVVRelationSerializer(data=mccr_ovv_relation)
        return serializer

    def get_serialized_for_existent(self, request, mccr_registry):
        data = JSONParser().parse(request)
        serialized_mccr = MCCRRegistrySerializerCreate(mccr_registry, data=data)
        return serialized_mccr

    def get_one(self, str_uuid):
        f_uuid = uuid.UUID(str_uuid)
        return MCCRRegistry.objects.get(pk=f_uuid)

    def serialize_and_save_files(self, request, mccr_id):
        for f in request.data.getlist("files[]"):
            serialized_file = self.get_serialized_mccr_file(mccr_id, request.user.id, f)
            if serialized_file.is_valid():
                serialized_file.save()

    # TODO: Handle exception
    def create(self, request):
        serialized_mccr = self.get_serialized_mccr(request)
        if serialized_mccr.is_valid():
            new_mccr = serialized_mccr.save()
            if new_mccr.id:
                # TODO: check operation to revert
                self.serialize_and_save_files(request, new_mccr.id)
            return (True, MCCRRegistrySerializerCreate(new_mccr).data)
        return (False, serialized_mccr.errors)

    def get(self, id):
        try:
            mccr = self.get_one(id)
            serialized_mccr = MCCRRegistrySerializerView(mccr)
            content = serialized_mccr.data
            content['files'] = self._get_files_list(mccr.files)
            result = (True, content)
        except MCCRRegistry.DoesNotExist:
            result = (False, {"error": self.MCCR_ERROR_NOT_EXIST})
        return result

    def get_all(self):
        try:
            m_list = [
                {
                    'id': m.id,
                    'status': m.status,
                    'user_id': m.user.id,
                    'user': m.user.username,
                    'mitigation_id': m.mitigation.id,
                    'mitigation': m.mitigation.name,
                    'user_type_id': m.user_type.id,
                    'user_type': m.user_type.name,
                    'files': MCCRFile.objects.filter(mccr_id=m.id).count()
                } for m in MCCRRegistry.objects.all()
            ]
            result = (True, m_list)
        except MCCRRegistry.DoesNotExist:
            result = (False, self.MCCR_ERROR_GET_ALL)
        return result

    def get_form_data(self):
        try:
            mitigation_list = [
                {
                    "id": str(m.id),
                    "name": m.name,
                } for m in Mitigation.objects.all()
            ]
            user_types_list = [
                {
                    "id": str(u.id),
                    "name": u.name,
                } for u in MCCRUserType.objects.all()
            ]
            final_result = {
                "mitigations": mitigation_list,
                "user_types": user_types_list,
            }
            result = (True, final_result)
        except Mitigation.DoesNotExist:
            result = (False, {"error": self.MCCR_ERROR_EMPTY_MITIGATIONS_LIST})
        except:
            result = (False, {"error": self.MCCR_ERROR_UNKNOWN_MITIGATION_LIST})
        return result

    def get_all_ovv(self):
        try:
            ovv_list = [
                {
                    "id": o.id,
                    "email": o.email,
                    "phone": o.phone
                } for o in OVV.objects.all()
            ]
            result = (True, ovv_list, )
        except OVV.DoesNotExist:
            result = (False, {"error": self.MCCR_ERROR_EMPTY_OVV_LIST})
        except:
            result = (False, {"error": self.MCCR_ERROR_UNKNOWN_MITIGATION_LIST})
        return result

    # TODO: handle exception when id not exist
    def update(self, id, request):
        mccr_registry = self.get_one(id)
        serialized_mccr = self.get_serialized_for_existent(request, mccr_registry)
        if serialized_mccr.is_valid():
            result = (True, MCCRRegistrySerializerCreate(serialized_mccr.save()).data)

            if serialized_mccr.data.get('status')=="approved" and self.validate_user_group(request.user, 'OVV')==True:
                url = "http://{0}{1}".format(request.META['HTTP_HOST'], reverse('redirect_notification', kwargs={'mccr_id': mccr_registry.id}))
                message = self.buil_message_mccr(mccr_registry)
                self.sendStatusNotification("Executive Secretary", str(mccr_registry.id), message, url)
        else:
            result = (False, serialized_mccr.errors)
        return result

    def update_mccr_ovv_relation(self, mccr_id, ovv_id):
        serialized_mccr_ovv_relation = self.get_serialized_mccr_ovv_relation(mccr_id, ovv_id)
        if serialized_mccr_ovv_relation.is_valid():
            # TODO: should check if we have a previous registered status for the tuple mccr,ovv
            serialized_mccr_ovv_relation.save()
            result = (True, serialized_mccr_ovv_relation.data)
        else:
            result = (False, serialized_mccr_ovv_relation.errors)
        return result

    def delete(self, id):
        try:
            mccr = self.get_one(id)
            mccr.delete()
            result = True
        except MCCRRegistry.DoesNotExist:
            result = False
        return result

    def get_file_content(self, mccr_id, mccr_file_id):
        mccr_file = MCCRFile.objects.get(pk=mccr_file_id)
        path, filename = os.path.split(mccr_file.file.name)
        return (filename, BytesIO(self.storage.get_file(mccr_file.file.name)),)

    def download_file(self, mccr_id, mccr_file_id):
        return self.get_file_content(mccr_id, mccr_file_id)

    def _get_files_list(self, file_list):
        return [{'name': self._get_filename(f.file.name), 'file': self._get_file_path(str(f.mccr.id), str(f.id))} for f in file_list.all() ]

    def _get_file_path(self, mccr_id, mccr_file_id):
        url = reverse("get_mccr_file_version", kwargs={'id': mccr_id, 'mccr_file_id': mccr_file_id})
        return url

    def _get_filename(self, filename):
        fpath, fname = os.path.split(filename)
        return fname
    

    ##email services
    def sendNotification(self, recipient_list, subject, message_body):

        result = ses_service.send_notification(recipient_list, subject, message_body)
        
        return result
            
    def sendStatusNotification(self, group, subject, message_body, link):

        """first implementation"""
        subject = "MCCR approved: " + subject
        message_body += "<br>Detalles en <a href=" + link + ">ver más</a>"
        recipient_list = self.get_user_by_group(group)
        result = self.sendNotification(recipient_list, subject, message_body)

        return result

    def get_user_by_group(self, user_group):
        list = []
        for user in User.objects.filter(groups__name=user_group):
            list.append(user.email)
        return list

    def validate_user_group(self, user, user_group):
        result = False
        for g in user.groups.all():
            if g.name == user_group:
                result=True
        return  result

    def buil_message_mccr(self, data):
        id = "<p><b>Código: </b>{0}</p>".format(str(data.id))
        mitigation = "<p><b>Acción de mitigación: </b>{0}</p>".format(str(data.mitigation.name))
        status = "<p><b>Status: </b>{0}</p>".format(str(data.status))
        message = "<h3>Datos Generales</h3> {0} {1} {2}".format(id,mitigation,status)
        return message