# from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('register/', views.MyRegister.as_view(), name='register'),
    path('login/', views.MyLogin.as_view(), name='login'),
    path('logout/', views.my_logout, name='logout'),
    path("profile/<int:user_id>/", views.ShowProfileDetail.as_view()),
    path('', views.index, name='index'),
    path('home/', views.home, name='home'),
    path('host/', views.host, name='host'),
    path('profile/', views.Profile.as_view(), name='profile'),
    path('edit_profile/', views.edit_profile, name='edit profile'),
    path('change_password/', views.ChangePassword.as_view(), name='change password'),
    path('underground/', views.Underground.as_view(), name='Underground'),
    path("my_orders/", views.MyOrder.as_view()),
]
