from django.contrib import admin
from .models import ProductToUser, Dish, Ingredients
# Register your models here.


admin.site.register(ProductToUser)
admin.site.register(Dish)
admin.site.register(Ingredients)