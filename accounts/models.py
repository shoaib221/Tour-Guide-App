from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q


class Country(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name'], name="Unique Country")
        ]

    def __str__(self):
        return self.name


class City(models.Model):

    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    city = models.CharField(max_length=255)

    class Meta:
        constraints = [
            models.UniqueConstraint( fields=['country', 'city'], name='unique city')
        ]
        
    def __str__(self):
        return self.city


class UserDetail(User):
    mail = models.EmailField(max_length=255, blank=False)
    country = models.ForeignKey( Country , on_delete=models.CASCADE, blank=False)
    nid = models.CharField(max_length=20, blank=False)
    mobile = models.BigIntegerField(blank=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['nid'], name="Unique NID"),
            models.UniqueConstraint(fields=['mobile'], name="Unique Mobile Number"),
            models.UniqueConstraint(fields=['mail'], name="Unique Email Address"),
        ]


    def __str__(self):
        return self.username


class MyChoice:

    months = [
        (1, 'January'), (2, 'February'), (3,
                                          'March'), (4, 'April'), (5, 'May'), (6, 'June'),
        (7, 'July'), (8, 'August'), (9, 'September'), (10,
                                                       'Octobor'), (11, 'November'), (12, 'December')
    ]



