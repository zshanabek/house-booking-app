# Generated by Django 3.0.3 on 2020-02-25 14:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0013_auto_20200225_0458'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='iban',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]