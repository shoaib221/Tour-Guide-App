from django.urls import path, include
from . import views

urlpatterns = [

    path( 'all_house/', views.AllHouse.as_view(), name='all house'),
    path( 'house/<int:house_id>/', views.HouseDetail.as_view(), name='house detail'),
    path( 'register/', views.Register.as_view(), name='register'),
]