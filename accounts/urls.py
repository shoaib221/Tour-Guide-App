# from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('register/', views.MyRegister.as_view(), name='register'),
    path('login/', views.MyLogin.as_view(), name='login'),
    path('logout/', views.MyLogout.as_view(), name='logout'),
    path("profile/<int:user_id>/", views.ShowProfileDetail.as_view()),
    path('my_profile/', views.MyProfile.as_view(), name='profile'),
    path("home/", views.MyHome.as_view() ),
    path("update_name/", views.UpdateName.as_view() ),
    path("update_mail/", views.UpdateEmail.as_view() ),
    path("update_mobile/", views.UpdateMobile.as_view() ),
    path( "", views.MyLogin.as_view() ),
    path( "change_password/", views.ChangePassword.as_view() ),
    path( "forgot_password/", views.ForgotPassword.as_view(), name='forgot password'),
    path("test/", views.Test.as_view(), name="test")
]
