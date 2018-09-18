from rest_framework import serializers
from ppcn.workflow_steps.models import PPCNWorkflowStepFile, PPCNWorkflowStep


class PPCNWorkflowStepSerializer(serializers.ModelSerializer):
    class Meta:
        model = PPCNWorkflowStep
        fields = ('id', 'user', 'ppcn', 'name', 'entry_name', 'status')

class PPCNWorkflowStepFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = PPCNWorkflowStepFile
        fields = ('id', 'user', 'workflow_step', 'file')