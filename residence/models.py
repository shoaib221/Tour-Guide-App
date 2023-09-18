

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
            models.UniqueConstraint(fields=['user_detail', 'name'], name="Unique Room")
        ]

    def clean_fields(self, exclude=None):
        super().clean_fields(exclude=exclude)

        if not (exclude and "user_detail" in exclude):
            if House.objects.filter(user_detail=self.user_detail, name=self.name).exists():
                if House.objects.get(user_detail=self.user_detail, name=self.name).id != self.id:
                    raise ValidationError("You have already a residence of that name -_-")

    def __str__(self):
        return '%s\'s %s at %s' % (self.user_detail.__str__(), self.name, self.city.__str__())



class Room(models.Model):
    name = models.CharField(max_length=255)
    house = models.ForeignKey(House, on_delete=models.CASCADE, blank=False, default=None)
    beds= models.IntegerField(blank=False)
    has_ac = models.BooleanField(default=False, blank=False)
    price= models.FloatField(blank=False)
    description = models.CharField(max_length=255, null=True, blank=True, default=None)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=[ 'name' , 'house' ], name="Unique House")
        ]



    def clean_fields(self, exclude=None):
        super().clean_fields(exclude=exclude)

        if exclude and 'house' in exclude:
            pass
        else:
            if Room.objects.filter(house_id=self.house.id, name=self.name).exists():
                pass
                # print(self.id)
                if Room.objects.get(house=self.house, name=self.name).id != self.id:
                    raise ValidationError("This Residence has already a room of this name")


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
    book_from = models.DateField( blank=False )
    book_to = models.DateField( blank=False )
    total_price = models.FloatField( blank=False )
    booking_time = models.DateTimeField( blank=False )

    class Meta:
        pass
        


class RoomBooking(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, blank=False, default=None)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, blank=False, default=None)
    price = models.FloatField( blank=False,  default=None    )
    
    class Meta:
        pass


class Cart(models.Model):

    user_detail = models.ForeignKey(UserDetail, on_delete=models.CASCADE, blank=False, default=None)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, blank=False, default=None)
    house = models.ForeignKey(House, on_delete=models.CASCADE, blank=False, default=None)
    book_from = models.DateField( blank=False )
    book_to = models.DateField( blank=False )
    price = models.FloatField( blank=False )

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user_detail', 'room' ], name="Unique Cart")
        ]



# pip install Pillow
# python manage.py makemigrations
# python manage.py sqlmigrate @appname @migrationid
# python manage.py migrate
# django admin username-shoaib password-1234
# python manage.py createsuperuser @username
# python manage.py changepassword @username
# python manage.py createsuperuser -h
