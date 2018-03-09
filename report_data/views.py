from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import ReportFile
from .serializers import ReportFileSerializer


@api_view(['GET', 'DELETE', 'PUT'])
def get_delete_update_report_file(request, pk):
    try:
        report = ReportFile.objects.get(pk=pk)
    except ReportFile.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    # get details of a single puppy
    if request.method == 'GET':
        serializer = ReportFileSerializer(report)
        return Response(serializer.data)
    # delete a single puppy
    elif request.method == 'DELETE':
        report.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    # update details of a single puppy
    elif request.method == 'PUT':
        serializer = ReportFileSerializer(report, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def get_post_report_files(request):
    # get all puppies
    if request.method == 'GET':
        report_files = ReportFile.objects.all()
        serializer = ReportFileSerializer(report_files, many=True)
        return Response(serializer.data)
    # insert a new record for a puppy
    elif request.method == 'POST':
        data = {
            'name': request.data.get('name'),
            'file_name': request.data.get('file_name'),
        }
        serializer = ReportFileSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

