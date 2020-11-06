from django.db import models

CATEGORIES = (('breads', 'breads'),
              ('cereals', 'cereals'),
              ('diary', 'diary'),
              ('drinks', 'drinks'),
              ('fish and seafood', 'fish and seafood'),
              ('fruits and vegetables', 'fruits and vegetables'),
              ('meat', 'meat'),
              ('mushrooms', 'mushrooms'),
              ('nuts and seeds', 'nuts and seeds'),
              ('oils', 'oils'),
              ('pastas', 'pastas'),
              ('sweets', 'sweets'),
              ('others', 'others'))

class Products(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=100, choices=CATEGORIES)
    calories = models.PositiveIntegerField()
    proteins = models.DecimalField(decimal_places=1, max_digits=10)
    carbohydrates = models.DecimalField(decimal_places=1, max_digits=10)
    sugars = models.DecimalField(decimal_places=1, max_digits=10)
    fats = models.DecimalField(decimal_places=1, max_digits=10)

    class Meta:
        constraints = [models.CheckConstraint(check=models.Q(carbohydrates__gte=models.F('sugars')), name="Mass of sugars cannot be higher than mass of carbohydrates"), models.CheckConstraint(check=models.Q(proteins__lte=(100 - models.F("carbohydrates") - models.F("fats"))), name="Sum of proteins, carbohydrates and fat cannot be greater than 0")]

    def __str__(self):
        return self.name
