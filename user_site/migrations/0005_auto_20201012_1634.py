# Generated by Django 3.1.2 on 2020-10-12 14:34

from django.db import migrations, models
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('user_site', '0004_auto_20201012_1603'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dish',
            name='ingredients',
            field=jsonfield.fields.JSONField(default={'mass': 0, 'name': ''}),
        ),
        migrations.AlterField(
            model_name='userfooddatabase',
            name='name',
            field=models.CharField(max_length=100),
        ),
    ]
