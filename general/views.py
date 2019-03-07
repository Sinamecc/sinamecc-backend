from rest_framework.decorators import api_view, parser_classes
from rest_framework.response import Response
from rest_framework import status
from users.services import UserService
from general.serializers import UserSerializer
from general.helpers import ViewHelper

service = UserService()
view_helper = ViewHelper(service)

# Create your views here.
@api_view(['GET'])
def get_user_info_by_name(request, username):
    if request.method == "GET":
        return view_helper.get_one(username)