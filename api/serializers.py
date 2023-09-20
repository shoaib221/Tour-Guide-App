
from rest_framework import serializers
from residence.models import *
from accounts.models import *



class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = [ 'name' ]
    
class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = '__all__'


###########################################

class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDetail
        fields = [ 'mail', 'mobile', 'nid', 'country', 'password' ]


class LoginSerializer(serializers.Serializer):
    mail = serializers.CharField( required=True )
    password = serializers.CharField( required=True )


class MyProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDetail
        fields = [ 'mail', 'mobile', 'nid', 'country' ]


########################################################################

class HouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = House
        fields = [ 'name', 'address', 'city', 'description' ]