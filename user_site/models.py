from django.db import models
from django.contrib.auth.models import User
from food_database.models import CATEGORIES, Products

DAYS = (('monday', 'monday'),
        ('tuesday', 'tuesday'),
        ('wednesday', 'wednesday'),
        ('thursday', 'thursday'),
        ('friday', 'friday'),
        ('saturday', 'saturday'),
        ('sunday', 'sunday'))


class ProductToUser(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)

    def __str__(self):
        return self.product.name


class Dish(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, default='Dish')
    day = models.CharField(max_length=10, choices=DAYS)
    time = models.TimeField()

    class Meta:
        unique_together = [('day', 'time', 'user'), ('day', 'name', 'user')]

    def __str__(self):
        return f"{self.user}'s {self.day} {self.name}"


class Ingredients(models.Model):
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(ProductToUser, on_delete=models.CASCADE)
    mass = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.mass} g of {self.ingredient} in {self.dish}"