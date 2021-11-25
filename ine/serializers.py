from rest_framework import serializers
from ine.models import dict_ccaa, dict_provinces, dict_municipalities

class dict_ccaa_Serializer(serializers.ModelSerializer):
    class Meta:
        model = dict_ccaa
        fields = ('CODAUTO', 'NOMBRE')

class dict_provinces_Serializer(serializers.ModelSerializer):
    class Meta:
        model = dict_provinces
        fields = ('CPRO', 'NOMBRE')

class dict_municipalities_Serializer(serializers.ModelSerializer):
    class Meta:
        model = dict_municipalities
        fields = ('CODAUTO', 'CPRO', 'CMUN', 'DC', 'NOMBRE')
