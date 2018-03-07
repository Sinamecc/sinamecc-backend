from rest_framework import serializers
from .models import ReportFile


class ReportFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportFile
        fields = ('name', 'file_name', 'created', 'updated')