# Generated by Django 2.2.7 on 2019-12-11 18:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('house', '0008_auto_20191211_2349'),
    ]

    operations = [
        migrations.RenameField(
            model_name='nearbuildinghouse',
            old_name='nearbuilding',
            new_name='near_building',
        ),
    ]
