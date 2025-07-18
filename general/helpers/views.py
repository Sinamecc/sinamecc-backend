from django.http import FileResponse
from rest_framework import status
from rest_framework.response import Response


class ViewHelper():
    def __init__(self, service):
        self.service = service

    def get_one(self, *args):
        result_status, result_data = self.service.get(*args)
        if result_status:
            result = Response(result_data)
        else:
            result = Response(result_data, status=status.HTTP_404_NOT_FOUND)
        return result

    def get_by_name(self,  *args):
        method_to_call = getattr(self.service, args[0])
        result_status, result_data = method_to_call(*args[1:])
        if result_status:
            result = Response(result_data)
        else:
            result = Response(result_data, status=status.HTTP_400_BAD_REQUEST)
        return result

    def get_all(self, *args):
        return self.get_by_name("get_all", *args)

    def get_form_data(self, *args):
        return self.get_by_name("get_form_data", *args)

    def delete(self, *args):
        
        result_status, result_data = self.service.delete(*args)
        if result_status:
            result = Response(result_data, status=status.HTTP_200_OK)
        else:
            result = Response(result_data, status=status.HTTP_404_NOT_FOUND)

        return result

    def download_file(self, parent_id, file_id):
        file_name, file_data = self.service.download_file(parent_id, file_id)
        attachment_file_name_value = "attachment; filename=\"{}\"".format(file_name)
        response = FileResponse(file_data, content_type='application/octet-stream')
        response.setdefault('Content-Disposition', attachment_file_name_value)
        return response

    
    def call_download_file_method(self, method, *args, **kwargs):
        
        method_to_call = getattr(self.service, method)
        result_status, result_data = method_to_call(*args, **kwargs)
        if result_status:
            filename = result_data[0]
            content = result_data[1]
            attachment_file_name_value = "attachment; filename=\"{}\"".format(filename)
            result = FileResponse(content,content_type='application/octet-stream')
            result.setdefault('Content-Disposition', attachment_file_name_value)

        else:
            result = self.error_message(result_data)
        
        return result
    
    
    def execute_by_name(self, *args):
        method_to_call = getattr(self.service, args[0])
        result_status, result_data = method_to_call(*args[1:])
        if result_status:
            result = Response(result_data, status=status.HTTP_200_OK)
        else:
            result = Response(result_data, status=status.HTTP_400_BAD_REQUEST)
        return result

    def post(self, request):
        save_result, result_detail = self.service.create(request)
        if save_result:
            result = Response(result_detail, status=status.HTTP_201_CREATED)
        else:
            result = Response(result_detail, status=status.HTTP_400_BAD_REQUEST)
        return result

    def put(self, *args):
        result_status, result_data = self.service.update(*args)
        if result_status:
            result = Response(result_data)
        else:
            result = Response(result_data, status=status.HTTP_400_BAD_REQUEST)
        return result
    
    def patch(self, id, request):

        result_status, result_data = self.service.patch(id, request)
        if result_status:
            result = Response(result_data)
        else:
            result = Response(result_data, status=status.HTTP_400_BAD_REQUEST)
        return result

    def error_message(self, message):
        error_message = {"error": message}
        return Response(error_message, status=status.HTTP_400_BAD_REQUEST)
