# Generated by Django 2.2.7 on 2020-02-04 19:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0010_reservation_days'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='is_paid',
            field=models.BooleanField(default=False),
        ),
    ]
