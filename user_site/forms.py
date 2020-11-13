from django import forms
from food_database.models import Products, CATEGORIES
from .models import Ingredients, ProductToUser
from django.db.models import Q

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


def create_new_ingredient_form_set(request):

    class NewIngredient(forms.ModelForm):

        user = request.user

        ingredient = forms.ModelChoiceField(queryset=ProductToUser.objects.filter(Q(user=1) | Q(user=user)))
        mass = forms.IntegerField(min_value=1)

        class Meta:
            model = Ingredients
            exclude = {'dish'}

    IngredientFormSet = forms.modelformset_factory(Ingredients, form=NewIngredient, extra=1)

    return IngredientFormSet


