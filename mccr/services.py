from mitigation_action.models import Mitigation
from mccr.models import MCCRRegistry, MCCRUserType, MCCRFile
from mccr.serializers import MCCRRegistrySerializer, MCCRFileSerializer
from rest_framework.parsers import JSONParser
import datetime
import uuid


# TODO: Change is_valid() to exception
class MCCRService():
    def __init__(self):
        self.MCCR_ERROR_NOT_EXIST = "MCCR does not exists"
        self.MCCR_ERROR_GET_ALL = "Error retrieving all MCCR records"
        self.MCCR_ERROR_EMPTY_MITIGATIONS_LIST = "Empty mitigation actions list"
        self.MCCR_ERROR_UNKNOWN_MITIGATION_LIST = "Unknown error retrieving mitigation actions list"

    def get_serialized_mccr(self, request):
        d = {
            "status": request.data.get("status"),
            "user": request.user.id,
            "mitigation": request.data.get("mitigation"),
            "user_type": request.data.get("user_type")
        }
        serialized_mccr = MCCRRegistrySerializer(data=d)
        return serialized_mccr

    def get_serialized_mccr_file(self, mccr_id, user_id, file):
        file_list = {
                "file": file,
                "user": user_id,
                "mccr": mccr_id
            }
        serializer = MCCRFileSerializer(data=file_list)
        return serializer

    def get_serialized_for_existent(self, request, mccr_registry):
        data = JSONParser().parse(request)
        serialized_mccr = MCCRRegistrySerializer(mccr_registry, data=data)
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
            return (True, MCCRRegistrySerializer(new_mccr).data)
        return (False, serialized_mccr.errors)

    def get(self, id):
        try:
            serialized_mccr = MCCRRegistrySerializer(self.get_one(id))
            result = (True, serialized_mccr.data)
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

    # TODO: handle exception when id not exist
    def update(self, id, request):
        mccr_registry = self.get_one(id)
        serialized_mccr = self.get_serialized_for_existent(request, mccr_registry)
        if serialized_mccr.is_valid():
            result = (True, MCCRRegistrySerializer(serialized_mccr.save()).data)
        else:
            result = (False, serialized_mccr.errors)
        return result

    def delete(self, id):
        try:
            mccr = self.get_one(id)
            mccr.delete()
            result = True
        except MCCRRegistry.DoesNotExist:
            result = False
        return result
