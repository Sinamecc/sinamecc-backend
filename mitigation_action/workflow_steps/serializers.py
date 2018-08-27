from rest_framework import serializers
from mitigation_action.workflow_steps.models import MAWorkflowStepFile, MAWorkflowStep
from mitigation_action.models import Mitigation

class MAWorkflowStepSerializer(serializers.ModelSerializer):
    class Meta:
        model = MAWorkflowStep
        fields = ('user', 'mitigation_action', 'name', 'entry_name', 'status')

class MAWorkflowStepFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = MAWorkflowStepFile
        fields = ('user', 'workflow_step', 'file')