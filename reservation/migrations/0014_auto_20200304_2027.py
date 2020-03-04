# Generated by Django 3.0.3 on 2020-03-04 14:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0013_auto_20200227_0329'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='status',
            field=models.IntegerField(choices=[(0, 'Request'), (1, 'Approved'), (2, 'Rejected'), (3, 'Paid'), (4, 'Canceled'), (5, 'Expired'), (6, 'Inactive')], default=0),
        ),
    ]