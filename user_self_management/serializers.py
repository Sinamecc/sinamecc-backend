from rest_framework import serializers
from user_self_management.models import User, Module

class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = ('name', 'supplier_reviewer')

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'institution', 'role', 'position', 'module')
    
    def to_representation(self, instance):
        data =  super().to_representation(instance)
        data['module'] = ModuleSerializer(instance.module.all(), many=True).data
        return data