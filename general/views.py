from rest_framework.decorators import api_view, parser_classes
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from general.serializers import UserSerializer

# Create your views here.
@api_view(['GET'])
def get_user_info_by_name(request, username):
    UserModel = get_user_model()
    try:
        user = UserModel.objects.filter(username=username).get()
    except UserModel.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = UserSerializer(user)
        return Response(serializer.data)
