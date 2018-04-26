from rest_framework.decorators import api_view, parser_classes
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework import status
from report_data.models import ReportFile, ReportFileVersion
from report_data.serializers import ReportFileSerializer, ReportFileVersionSerializer
from report_data.services import get_all_report_files, build_report_file_serializer, create_report_file, get_all_file_versions, get_report_file, update_report_file


@api_view(['GET', 'DELETE', 'PUT'])
def get_delete_update_report_file(request, pk):
    try:
        report = ReportFile.objects.get(pk=pk)
    except ReportFile.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ReportFileSerializer(report)
        return Response(serializer.data)
    
    elif request.method == 'DELETE':
        report.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    elif request.method == 'PUT':
        if update_report_file(request, report):
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_report_file_versions(request, pk):
    try:
        report = get_report_file(pk)
    except ReportFile.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        versions = get_all_file_versions(report)
        return Response(versions)

@api_view(['GET', 'POST'])
@parser_classes((MultiPartParser, FormParser, JSONParser,))
def get_post_report_files(request):
    if request.method == 'GET':
        report_files = get_all_report_files()
        return Response(report_files)
    elif request.method == 'POST':
        serializer = build_report_file_serializer(request)
        if create_report_file(request, serializer):
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
