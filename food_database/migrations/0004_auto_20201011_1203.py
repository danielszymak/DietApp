# Generated by Django 3.1.2 on 2020-10-11 10:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('food_database', '0003_auto_20201011_1138'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fooddatabase',
            name='category',
            field=models.CharField(choices=[('breads', 'breads'), ('cereals', 'cereals'), ('diary', 'diary'), ('drinks', 'drinks'), ('fish and seafood', 'fish and seafood'), ('fruits and vegetables', 'fruits and vegetables'), ('meat', 'meat'), ('nuts and seeds', 'nuts and seeds'), ('pastas', 'pastas'), ('sweets', 'sweets'), ('others', 'others')], max_length=100),
        ),
    ]