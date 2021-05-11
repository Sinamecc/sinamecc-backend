from django.utils.translation import override
from rest_framework import serializers
from mitigation_action.models import Finance, MitigationAction, Contact, Status, FinanceSourceType, GeographicScale,\
    InitiativeType, FinanceStatus, InitiativeGoal, Initiative, MitigationActionStatus, GeographicLocation


##
## Auxiliar Class Serializer
##
class GenericListSerializer(serializers.ListSerializer):
    def update(self, instance, validated_data):
        # Maps for id->instance and id->data item.
        record_mapping = {record.id: record for record in instance}
        data_mapping = {}
        new_record_list = []

        for item in validated_data:
            if item.get('id', False):
                data_mapping[item.get('id')] = item
            else:
                new_record_list.append(item)

        # Perform creations and updates.
        ret = []

        for record_id, data in data_mapping.items():
            record = record_mapping.get(record_id, None)
            if record is None:
                ret.append(self.child.create(data))
            else:
                ret.append(self.child.update(record, data))

        for data in new_record_list:
            ret.append(self.child.create(data))


        # Perform deletions.
        for record_id, record in record_mapping.items():
            if record_id not in data_mapping:
                record.delete()

        return ret


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


##
## Start Model Serializers
##

class FinanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Finance
        fields = ('id', 'status', 'administration', 'source', 'source_description', 'reference_year', 'budget',
                    'mideplan_registered', 'executing_entity')


class InitiativeGoalSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    class Meta:
        model = InitiativeGoal
        fields = ('id', 'goal', 'initiative')
        list_serializer_class = GenericListSerializer
        

class InitiativeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Initiative
        fields = ('id', 'name', 'objective', 'description', 'initiative_type')

    def to_representation(self, instance):

        data = super().to_representation(instance)
        data['initiative_type'] = InitiativeTypeSerializer(instance.initiative_type).data
        data['goal'] = InitiativeGoalSerializer(instance.goal.all(), many=True).data

        return data


class MitigationActionStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = MitigationActionStatus
        fields = ('id', 'status', 'start_date', 'end_date', 'other_end_date', 'institution', 'other_institution')

    def to_representation(self, instance):

        data = super().to_representation(instance)
        data['status'] = StatusSerializer(instance.status).data
        
        return data


class GeographicLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeographicLocation
        fields = ('id', 'geographic_scale', 'location')

    def to_representation(self, instance):

        data = super().to_representation(instance)
        data['geographic_scale'] = GeographicScaleSerializer(instance.geographic_scale).data

        return data


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ('id', 'institution', 'full_name', 'job_title', 'email', 'phone', 'user', 'created', 'updated')


class MitigationActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = MitigationAction
        fields = ('id', 'fsm_state','contact', 'initiative', 'status_information', 'geographic_location', 'user', 'created', 'updated')

    def to_representation(self, instance):

        data = super().to_representation(instance)
        data['contact'] = ContactSerializer(instance.contact).data
        data['initiative'] = InitiativeSerializer(instance.initiative).data
        data['status_information'] = MitigationActionStatusSerializer(instance.status_information).data
        data['geographic_location'] = GeographicLocationSerializer(instance.geographic_location).data

        return data




