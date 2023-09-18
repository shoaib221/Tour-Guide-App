from django.urls import path, include
from . import views

urlpatterns = [
    path('register/', views.MyRegister.as_view(), name='api register')
]

'''
    path('login/', views.MyLogin.as_view(), name='login'),
    path('logout/', views.MyLogout.as_view(), name='logout'),
    path("profile/<int:user_id>/", views.ShowProfileDetail.as_view()),
    path('my_profile/', views.MyProfile.as_view(), name='profile'),
    path("home/", views.MyHome.as_view() ),
    path("update_name/", views.UpdateName.as_view() ),
    path("update_mail/", views.UpdateEmail.as_view() ),
    path("update_mobile/", views.UpdateMobile.as_view() ),
    path( "", views.MyLogin.as_view()    ),
    path( "change_password/", views.ChangePassword.as_view()    ),
    path( "forgot_password/", views.ForgotPassword.as_view(), name='forgot password'),
    path( 'my_house/', views.MyHouse.as_view(), name='my residence'),
    path( 'add_house/', views.AddHouse.as_view(), name='add residence'),
    path( 'house/<int:id>/', views.HouseDetail.as_view(), name='residence detail'),
    path( 'house/<int:id>/addroom/', views.AddRoom.as_view() , name='add room'),
    path( 'room/<int:id>/', views.RoomDetail.as_view() , name='room detail'),
    path( 'order/<int:id>/', views.OrderDetail.as_view() , name='order detail'),
    path( 'room/<int:room_id>/create_unavail/', views.CreateUnavailability.as_view(), name='create room availability'),
    path( 'del_unavail/<int:id>/', views.DeleteUnavailability.as_view(), name='room unavailabilities'),
    path( 'search_vacancy/', views.SearchRoom.as_view(), name='search room'),
    path( 'add_to_cart/<int:room_id>/', views.AddToCart.as_view(), name='search room detail'),
    path( 'go_to_cart/', views.MyCart.as_view(), name='cart'),
    path( 'book/', views.BookRooms.as_view(), name='book'),
    path( 'my_booking/', views.MyBookings.as_view(), name='my booking'),

    '''