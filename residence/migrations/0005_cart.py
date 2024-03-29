# Generated by Django 4.2.5 on 2023-09-11 06:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
        ('residence', '0004_roomunavailable_remove_roomcart_room_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('book_from', models.DateField()),
                ('book_to', models.DateField()),
                ('price', models.FloatField()),
                ('house', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='residence.house')),
                ('room', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='residence.room')),
                ('user_detail', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='accounts.userdetail')),
            ],
        ),
    ]
