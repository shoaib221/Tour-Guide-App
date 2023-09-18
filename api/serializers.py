
from rest_framework import serializers
from residence.models import *
from accounts.models import *

class HouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = House
        fields = '__all__'

class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDetail
        fields = [ 'mail', 'mobile', 'nid', 'country' ]

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'