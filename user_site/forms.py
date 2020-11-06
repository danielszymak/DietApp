from django import forms
from food_database.models import Products, CATEGORIES
from .models import Ingredients

DAYS = (('monday', 'monday'),
        ('tuesday', 'tuesday'),
        ('wednesday', 'wednesday'),
        ('thursday', 'thursday'),
        ('friday', 'friday'),
        ('saturday', 'saturday'),
        ('sunday', 'sunday'))


class FoodSearch(forms.Form):
    name = forms.CharField(max_length=100, required=False, label="You are looking for a product? Put it's name here:")


class NewProduct(forms.Form):
    name = forms.CharField(label="Name", max_length=100)
    category = forms.ChoiceField(choices=CATEGORIES, label="Category")
    proteins = forms.DecimalField(label="Proteins", decimal_places=1, max_digits=10, min_value=0, max_value=100)
    carbohydrates = forms.DecimalField(label="Carbohydrates", decimal_places=1, max_digits=10, min_value=0, max_value=100)
    sugars = forms.DecimalField(label="Sugars", decimal_places=1, max_digits=10, min_value=0, max_value=100)
    fats = forms.DecimalField(label="Fats", decimal_places=1, max_digits=10, min_value=0, max_value=100)


class NewDish(forms.Form):
    name = forms.CharField(label="Name", max_length=100)
    day = forms.ChoiceField(label="Day", choices=DAYS)
    time = forms.TimeField(label="Time", help_text='Format: hh:mm - seconds are ignored')


class NewIngredient(forms.Form):
    ingredient = forms.ModelChoiceField(queryset=Products.objects.all())
    mass = forms.IntegerField(min_value=0)


# NewIngredientFormSet = forms.formset_factory(NewIngredient, extra=1)

NewIngredientFormSet = forms.modelformset_factory(Ingredients, exclude={'dish'}, extra=1)


