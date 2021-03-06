# Generated by Django 3.1.2 on 2020-11-06 09:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('food_database', '0008_auto_20201030_2125'),
        ('user_site', '0015_auto_20201105_1808'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredients',
            name='ingredient',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='food_database.products'),
        ),
        migrations.AlterField(
            model_name='ingredients',
            name='mass',
            field=models.PositiveIntegerField(blank=True),
        ),
    ]
