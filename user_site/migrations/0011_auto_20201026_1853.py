# Generated by Django 3.1.2 on 2020-10-26 17:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_site', '0010_auto_20201023_1620'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userfooddatabase',
            name='category',
            field=models.CharField(choices=[('breads', 'breads'), ('cereals', 'cereals'), ('diary', 'diary'), ('drinks', 'drinks'), ('fish and seafood', 'fish and seafood'), ('fruits and vegetables', 'fruits and vegetables'), ('meat', 'meat'), ('mushrooms', 'mushrooms'), ('nuts and seeds', 'nuts and seeds'), ('oils', 'oils'), ('pastas', 'pastas'), ('sweets', 'sweets'), ('others', 'others')], max_length=100),
        ),
    ]