from django.db import models
from django.db.models import fields
from rest_framework import serializers
from django.contrib.auth import get_user_model

from general.models import Address, Canton, Province, District

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'email', 'is_active')

class ProvinceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Province
        fields = ('id', 'code', 'name', 'created', 'updated')

class CantonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Canton
        fields = ('id', 'code', 'name', 'province', 'created', 'updated')

    def to_representation(self, instance):
        
        data = super().to_representation(instance)
        data['province'] = ProvinceSerializer(instance.province).data

        return data

class DistrictSerializer(serializers.ModelSerializer):

    class Meta:
        model = District
        fields = ('id', 'code', 'name', 'canton', 'created', 'updated')
    
    def to_representation(self, instance):
        
        data = super().to_representation(instance)
        data['canton'] = CantonSerializer(instance.canton).data

        return data

class AddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = Address
        fields = ('id', 'app_scale', 'description', 'GIS', 'district', 'canton', 'province', 'created', 'updated')

    def to_representation(self, instance):

        data = super().to_representation(instance)
        data['district'] = DistrictSerializer(instance.district.all(), many=True).data
        data['canton'] = CantonSerializer(instance.canton.all(), many=True).data
        data['province'] = ProvinceSerializer(instance.province.all(), many=True).data

        return data