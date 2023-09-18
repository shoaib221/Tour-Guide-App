from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from residence.models import House
from .serializers import *
from accounts.models import UserDetail, Country

###########################################  accounts  ###########################################

class Register(APIView):

    def get(self, request):
        
        serializer = UserDetailSerializer()
        qs = Country.objects.all()
        country_serializer = CountrySerializer(qs, many=True)
        context = {
            'user_detail': serializer.data,
            'country': country_serializer.data
        }
        return Response(context)

    def post(self, request):
        serializer = UserDetailSerializer(data=request.data)

        if serializer.is_valid():
            print("valid")
            user_detail = serializer.save(commit=False)
            user_detail.username = user_detail.mail
            try:
                serializer.save()
                return Response({'message': 'User Created'}, status=status.HTTP_201_CREATED)
            except ValidationError as e:
                return Response({'message': e}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Create your views here.

class AllHouse(APIView):
    def get(self, request):
        all_house = House.objects.all()
        serializer = HouseSerializer(all_house, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = HouseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data)
    
class HouseDetail(APIView):
    def get(self, request, house_id):
        house = House.objects.get(id=house_id)
        serializer = HouseSerializer(house)
        return Response(serializer.data)

    def put(self, request, house_id):
        house = House.objects.get(id=house_id)
        serializer = HouseSerializer(house, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.data)

    def delete(self, request, house_id):
        house = House.objects.get(id=house_id)
        house.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)