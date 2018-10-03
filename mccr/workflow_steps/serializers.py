from rest_framework import serializers
from mccr.workflow_steps.models import MCCRWorkflowStep,MCCRWorkflowStepFile


class MCCRWorkflowStepSerializer(serializers.ModelSerializer):
    class Meta:
        model = MCCRWorkflowStep
        fields = ('user', 'mccr', 'name', 'entry_name', 'status')

class MCCRWorkflowStepFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = MCCRWorkflowStepFile
        fields = ('user', 'workflow_step', 'file')