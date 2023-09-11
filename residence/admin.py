

from django.contrib import admin
from .models import House , Room, RoomUnavailable, RoomBooking, Booking


# Register your models here.
admin.site.register(House)
admin.site.register(Room)
admin.site.register(RoomBooking)
admin.site.register(RoomUnavailable)
admin.site.register(Booking)