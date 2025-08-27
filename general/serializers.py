from django.db import models
from django.db.models import fields
from rest_framework import serializers
from django.contrib.auth import get_user_model

from general.models import Address, Canton, Province, District, Dimension, Category, CategoryGroup, CategoryCT, Characteristic

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

class DimensionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Dimension
        fields = ('id', 'code', 'name', 'created', 'updated')


class CategoryGroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = CategoryGroup
        fields = ('id', 'code', 'name', 'dimension', 'created', 'updated')
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['dimension'] = DimensionSerializer(instance.dimension).data

        return data

class CategorySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Category
        fields = ('id', 'code', 'name', 'category_group', 'created', 'updated')
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['category_group'] = CategoryGroupSerializer(instance.category_group).data
        
        return data

class CategoryCTSerializer(serializers.ModelSerializer):

    class Meta:
        model = CategoryCT
        fields = ('id', 'code', 'name', 'created', 'updated')

class CharacteristicSerializer(serializers.ModelSerializer):

    class Meta:
        model = Characteristic
        fields = ('id', 'code', 'name', 'category_ct', 'created', 'updated')

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['category_ct'] = CategoryCTSerializer(instance.category_ct).data
        return data