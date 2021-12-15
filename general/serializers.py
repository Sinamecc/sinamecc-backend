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

class DistrictSerializer(serializers.ModelSerializer):

    class Meta:
        model = District
        fields = ('id', 'code', 'name', 'canton', 'created', 'updated')

class AddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = Address
        fields = ('id', 'description', 'GIS', 'district', 'created', 'updated')