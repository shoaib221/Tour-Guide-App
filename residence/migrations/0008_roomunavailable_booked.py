# Generated by Django 4.2.5 on 2023-09-18 05:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('residence', '0007_alter_booking_booking_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='roomunavailable',
            name='booked',
            field=models.BooleanField(default=False),
        ),
    ]