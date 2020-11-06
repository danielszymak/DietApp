from django.contrib import admin
from .models import Products
# Register your models here.


@admin.register(Products)
class DataAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'calories', 'proteins', 'carbohydrates', 'sugars', 'fats')
