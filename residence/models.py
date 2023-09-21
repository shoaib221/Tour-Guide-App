

from django.forms import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.postgres.fields import ArrayField
from django.db import models
from accounts.models import UserDetail, City, Country

#####################################         Models           ########################################################


class House(models.Model):

    user_detail = models.ForeignKey(UserDetail, blank=False,  on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    description = models.CharField(max_length=255, null=True, blank=True, default=None)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user_detail', 'name'], name="Unique House")
        ]

    def __str__(self):
        return '%s\'s %s at %s' % (self.user_detail.__str__(), self.name, self.city.__str__())



class Room(models.Model):
    name = models.CharField(max_length=255)
    house = models.ForeignKey(House, on_delete=models.CASCADE, blank=False, default=None)
    beds= models.IntegerField(blank=False)
    has_ac = models.BooleanField(default=False, blank=False)
    price_per_day = models.FloatField(blank=False)
    description = models.CharField(max_length=255, null=True, blank=True, default=None)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=[ 'name' , 'house' ], name="Unique Room")
        ]


class RoomUnavailable(models.Model):
    house = models.ForeignKey(House, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    from_day = models.DateField()
    to_day = models.DateField()
    booked = models.BooleanField(default=False, blank=False)

    class Meta:
        ordering = ["room", "from_day"]
        
    def clean_fields(self, exclude=None):
        super().clean_fields(exclude=exclude)


class Booking(models.Model):
    guest = models.ForeignKey(UserDetail, on_delete=models.CASCADE, blank=False, default=None)
    house = models.ForeignKey( House, on_delete=models.CASCADE, blank=False, default=None)
    total_price = models.FloatField( blank=False )
    booking_time = models.DateTimeField( blank=False )


class RoomBooking(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, blank=False, default=None )
    room = models.ForeignKey(Room, on_delete=models.CASCADE, blank=False, default=None )
    price = models.FloatField( blank=False,  default=None )
    start_date = models.DateField( blank=False, default=None )
    end_date = models.DateField( blank=False, default=None )


class Cart(models.Model):

    user_detail = models.ForeignKey(UserDetail, on_delete=models.CASCADE, blank=False, default=None)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, blank=False, default=None)
    house = models.ForeignKey(House, on_delete=models.CASCADE, blank=False, default=None)
    book_from = models.DateField( blank=False )
    book_to = models.DateField( blank=False )
    price = models.FloatField( blank=False, default=None )

