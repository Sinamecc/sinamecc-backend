from rest_framework.decorators import api_view, parser_classes
from rest_framework.response import Response
from rest_framework import status
from users.services import UserService
from rest_framework.exceptions import NotFound
from general.helpers import ViewHelper

service = UserService()
view_helper = ViewHelper(service)

# Create your views here.
@api_view(['GET'])
def get_user_info_by_name(request, username):
    if request.method == "GET":
        return view_helper.get_one(username)

@api_view(['GET'])
def handler404(request):
    result = { "error_code": 404, "error_message": "Page not found" }
    raise NotFound(detail=result, code=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def handler500(request):
    result = { "error_code": 500, "error_message": "Internal Server Error" }
    raise NotFound(detail=result, code=status.HTTP_500_INTERNAL_SERVER_ERROR)