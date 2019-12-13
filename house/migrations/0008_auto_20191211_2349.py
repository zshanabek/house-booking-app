# Generated by Django 2.2.7 on 2019-12-11 17:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('house', '0007_auto_20191211_1852'),
    ]

    operations = [
        migrations.AddField(
            model_name='house',
            name='beds',
            field=models.IntegerField(default=2),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='house',
            name='guests',
            field=models.IntegerField(default=2),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='accommodationhouse',
            name='house',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='house_accoms', to='house.House'),
        ),
        migrations.AlterField(
            model_name='nearbuildinghouse',
            name='house',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='house_near_buildings', to='house.House'),
        ),
        migrations.AlterField(
            model_name='nearbuildinghouse',
            name='nearbuilding',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='near_buildings', to='house.NearBuilding'),
        ),
        migrations.AlterField(
            model_name='rulehouse',
            name='house',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='house_rules', to='house.House'),
        ),
        migrations.CreateModel(
            name='FreeDateInterval',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_start', models.DateField(verbose_name='')),
                ('date_end', models.DateField(verbose_name='')),
                ('house', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='house_free_dates', to='house.House')),
            ],
        ),
    ]