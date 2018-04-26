from report_data.models import ReportFile, ReportFileVersion
from report_data.serializers import ReportFileSerializer, ReportFileVersionSerializer
import datetime
import os

def get_all_report_files():
    content = [
        {
            'id': r.id, 
            'user': r.user.id, 
            'name': r.name, 
            'created': r.created, 
            'updated': r.updated, 
            'last_active_version': r.reportfileversion_set.filter(active=True).first().version, 
            'versions': r.reportfileversion_set.all().count()
        } for r in ReportFile.objects.all()
    ]
    return content

def build_report_file_serializer(request):
    data = {
        'name': request.data.get('name'),
        'user': request.user.id,
    }
    serializer = ReportFileSerializer(data=data)
    return serializer

def build_report_file_version_serializer(request, report_file):
    version_str_format = 'report_data_%Y%m%d_%H%M%S'
    version_str = datetime.datetime.now().strftime(version_str_format)
    data = {
        'active': True,
        'version': version_str,
        'file': request.data.get('file'),
        'report_file': report_file.id,
        'user': request.user.id,
    }
    serializer = ReportFileVersionSerializer(data=data)
    return serializer

def create_report_file(request, serializer):
    if serializer.is_valid():
        report_file = serializer.save()
        version_serializer = build_report_file_version_serializer(request, report_file)
        if version_serializer.is_valid():
            version = version_serializer.save()
            report_file.reportfileversion_set.add(version)
            return True
    return False

def update_report_file(request, report):
    version_str_format = 'report_data_%Y%m%d_%H%M%S'
    version_str = datetime.datetime.now().strftime(version_str_format)
    data = {
        'name': request.data.get('name'),
        'user': request.user.id,
    }
    serializer = ReportFileSerializer(report, data=data)
    previous_version = report.reportfileversion_set.filter(active=True).first()
    previous_version_serializer = ReportFileVersionSerializer(previous_version, data={'active': False}, partial=True)
    if serializer.is_valid() and previous_version_serializer.is_valid():
        previous_version_serializer.save()
        report_file = serializer.save()
        version_data = {
            'active': True,
            'version': version_str,
            'file': request.data.get('file'),
            'report_file': report_file.id,
            'user': request.user.id,
        }
        version_serializer = ReportFileVersionSerializer(data=version_data)
        if version_serializer.is_valid():
            version = version_serializer.save()
            report_file.reportfileversion_set.add(version)
            return True
    return False

def get_report_file(pk):
    return ReportFile.objects.get(pk=pk)

def get_all_file_versions(report):
    versions_array = [
        {
        'version': v.version, 
        'file': os.path.relpath(v.file.name)
        } for v in report.reportfileversion_set.all()
    ]
    content = {
        'name': report.name,
        'versions': versions_array
    }
    return content
