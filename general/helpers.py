from rest_framework.response import Response
from rest_framework import status

class ViewHelper():
    def __init__(self, service):
        self.service = service

    def get_one(self, id):
        result_status, result_data = self.service.get(id)
        if result_status:
            result = Response(result_data)
        else:
            result = Response(result_data, status=status.HTTP_404_NOT_FOUND)
        return result

    def get_by_name(self, method_name):
        method_to_call = getattr(self.service, method_name)
        result_status, result_data = method_to_call()
        if result_status:
            result = Response(result_data)
        else:
            result = Response(result_data, status=status.HTTP_400_BAD_REQUEST)
        return result

    def get_all(self):
        return self.get_by_name("get_all")

    def get_form_data(self):
        return self.get_by_name("get_form_data")

    def execute_by_name(self, method_name, *args):
        method_to_call = getattr(self.service, method_name)
        result_status, result_data = method_to_call(*args)
        if result_status:
            result = Response(result_data)
        else:
            result = Response(result_data, status=status.HTTP_400_BAD_REQUEST)
        return result

    def delete(self, id):
        if self.service.delete(id):
            result = Response({"id": id}, status=status.HTTP_200_OK)
        else:
            result = Response({"id": id}, status=status.HTTP_404_NOT_FOUND)
        return result

    def post(self, request):
        save_result, result_detail = self.service.create(request)
        if save_result:
            result = Response(result_detail, status=status.HTTP_201_CREATED)
        else:
            result = Response(result_detail, status=status.HTTP_400_BAD_REQUEST)
        return result

    def put(self, id, request):
        result_status, result_data = self.service.update(id, request)
        if result_status:
            result = Response(result_data)
        else:
            result = Response(result_data, status=status.HTTP_400_BAD_REQUEST)
        return result

    def error_message(self, message):
        error_message = {"error": message}
        return Response(error_message, status=status.HTTP_400_BAD_REQUEST)
