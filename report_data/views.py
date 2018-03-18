from rest_framework.decorators import api_view, parser_classes
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework import status
from .models import ReportFile, ReportFileVersion
from .serializers import ReportFileSerializer, ReportFileVersionSerializer
import datetime
import os


@api_view(['GET', 'DELETE', 'PUT'])
def get_delete_update_report_file(request, pk):
    try:
        report = ReportFile.objects.get(pk=pk)
    except ReportFile.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    # get details of a single report_file
    if request.method == 'GET':
        serializer = ReportFileSerializer(report)
        return Response(serializer.data)
    # delete a single report_file
    elif request.method == 'DELETE':
        report.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    # update details of a single report_file
    elif request.method == 'PUT':
        serializer = ReportFileSerializer(report, data=request.data)
        previous_version = report.versions.filter(active=True).first()
        previous_version_serializer = ReportFileVersionSerializer(previous_version, data={'active': False}, partial=True)
        if serializer.is_valid() and previous_version_serializer.is_valid():
            previous_version_serializer.save()
            report_file = serializer.save()
            version_data = {
                'active': True,
                'version': os.path.relpath(report_file.file.name).replace("/", "_"),
                'file': os.path.relpath(report_file.file.name)
            }
            version_serializer = ReportFileVersionSerializer(data=version_data)
            if version_serializer.is_valid():
                version = version_serializer.save()
                report_file.versions.add(version)
                return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_report_file_versions(request, pk):
    try:
        report = ReportFile.objects.get(pk=pk)
    except ReportFile.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    # get versions details of a single report file
    if request.method == 'GET':
        versions_array = [{'version': v.version, 'file': v.file} for v in report.versions.all()]
        content = {
            'report_file_id': report.id,
            'report_file_name': report.name,
            'last_active_version': report.versions.filter(active=True).first().version,
            'versions': versions_array
        }
        return Response(content)

@api_view(['GET', 'POST'])
@parser_classes((MultiPartParser, FormParser, JSONParser,))
def get_post_report_files(request):
    # get all report_files
    if request.method == 'GET':
        report_files = ReportFile.objects.all()
        serializer = ReportFileSerializer(report_files, many=True)
        return Response(serializer.data)
    # insert a new record for a report_file and associate it a version
    elif request.method == 'POST':
        data = {
            'name': request.data.get('name'),
            'file': request.data.get('file')
        }
        serializer = ReportFileSerializer(data=data)
        if serializer.is_valid():
            report_file = serializer.save()
            version_data = {
                'active': True,
                'version': os.path.relpath(report_file.file.name).replace("/", "_"),
                'file': os.path.relpath(report_file.file.name)
            }
            version_serializer = ReportFileVersionSerializer(data=version_data)
            if version_serializer.is_valid():
                version = version_serializer.save()
                report_file.versions.add(version)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

