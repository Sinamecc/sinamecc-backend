from rest_framework import serializers
from mitigation_action.models import MitigationAction, Contact

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ('id','full_name', 'job_title', 'email', 'phone')

class MitigationSerializer(serializers.ModelSerializer):
    class Meta:
        model = MitigationAction
        fields = ('id', 'created', 'updated', 'user')

