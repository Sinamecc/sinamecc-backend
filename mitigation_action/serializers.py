from rest_framework import serializers
from mitigation_action.models import MitigationAction, Contact, Status, FinanceSourceType, GeographicScale,\
    InitiativeType, FinanceStatus

##
## Start Catalogs Serializers
##
class InitiativeTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = InitiativeType
        fields = ('id', 'code', 'name')


class GeographicScaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeographicScale
        fields = ('id', 'code', 'name')


class FinanceSourceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinanceSourceType
        fields = ('id', 'code','name')


class FinanceStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinanceStatus
        fields = ('id', 'code', 'name')


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = ('id', 'code', 'status')


##
## Finish Catalogs Serializers
##
class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ('id','full_name', 'job_title', 'email', 'phone', 'user', 'created', 'updated')


class MitigationSerializer(serializers.ModelSerializer):
    class Meta:
        model = MitigationAction
        fields = ('id', 'created', 'updated', 'user')

