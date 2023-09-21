from django.urls import path, include
from . import views

urlpatterns = [
    path('test/' , views.Test.as_view() , name='test' ),
    path('register/', views.MyRegister.as_view(), name='api register'),
    path('login/', views.MyLogin.as_view(), name='login'),
    path('logout/', views.MyLogout.as_view(), name='logout'),
    path('my_profile/', views.MyProfile.as_view(), name='profile'),
    path("profile/<int:user_id>/", views.ShowProfileDetail.as_view()),
    
    path("my_house/", views.MyHouse.as_view() ),
    path("add_house/", views.AddHouse.as_view() ),
    path("house/<int:house_id>/", views.HouseDetail.as_view() ),
    path("add_room/house/<int:house_id>/", views.AddRoom.as_view() ),
    path("room/<int:room_id>/", views.RoomDetail.as_view() ),

    path("create_unavail/room/<int:room_id>/", views.CreateUnavailability.as_view() ),
    path("del_unavail/<int:id>/", views.DeleteUnavailability.as_view() ),

    path("search_vacancy/", views.SearchRoom.as_view() ),
    path("my_cart/", views.MyCart.as_view() ),
    path("add_to_cart/", views.AddToCart.as_view() ),
    path("book/", views.BookRooms.as_view() ),

    path("bookings/house/<int:house_id>/", views.HouseBookings.as_view() ),
    path("bookings/room/<int:room_id>/", views.RoomBookings.as_view() ),
    path("my_bookings/", views.MyBookings.as_view() ),
]

