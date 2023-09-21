
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
        fields = '__all__'

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'


####################  Unavailability ###############################

class UnavailabilitySerializer(serializers.ModelSerializer):

    class Meta:
        model = RoomUnavailable
        fields = [ 'from_day', 'to_day' ]

class UnavailabilityDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = RoomUnavailable
        fields = '__all__'  

####################### Search  ######################################

class SearchRoomSerializer(serializers.Serializer):
    city = serializers.CharField( required=True )
    from_day = serializers.DateField( required=True )
    to_day = serializers.DateField( required=True )

class AddCart(serializers.Serializer):
    room_id = serializers.IntegerField( required=True )
    start_date = serializers.DateField( required=True )
    end_date = serializers.DateField( required=True )

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'
    
#######################################################################

class RoomBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomBooking
        fields = '__all__'

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'