from django.shortcuts import render, redirect, get_object_or_404
from .models import ProductToUser, Dish, Ingredients
from food_database.models import Products
from django.contrib.auth.decorators import login_required
from .forms import NewProduct, NewDish, FoodSearch, create_new_ingredient_form_set
from datetime import time
from django.db.models import Q
from django.db import IntegrityError


class Error(Exception):
    pass


@login_required
def food_table(request):

    food_data = []

    for row in ProductToUser.objects.filter(Q(user=request.user) | Q(user=1)):
        food_data.append(row.product)

    for item in range(len(food_data)-1, 0, -1):
        for i in range(item):
            if food_data[i].name.lower() > food_data[i+1].name.lower():
                (food_data[i], food_data[i+1]) = (food_data[i+1], food_data[i])

    # collecting data for get request
    selected_food_data = []

    if request.method == "GET":
        form = FoodSearch(data=request.GET)
        if form.is_valid():
            for item in food_data:
                if form.cleaned_data['name'] in item.name.lower():
                    selected_food_data.append(item)
    else:
        form = FoodSearch()

    return render(request, 'user_site/food_table.html', {'data': food_data,
                                                         'selected_data': selected_food_data,
                                                         'form': form})


@login_required
def my_products(request):

    userfood_data = []

    for row in ProductToUser.objects.all():
        if row.user == request.user:
            userfood_data.append(row.product)

    for item in range(len(userfood_data)-1, 0, -1):
        for i in range(item):
            if userfood_data[i].name.lower() > userfood_data[i+1].name.lower():
                (userfood_data[i], userfood_data[i+1]) = (userfood_data[i+1], userfood_data[i])

    # collecting data for get request
    selected_userfood_data = []

    if request.method == "GET":
        form = FoodSearch(data=request.GET)
        if form.is_valid():
            for item in userfood_data:
                if form.cleaned_data['name'] in item.name.lower():
                    selected_userfood_data.append(item)
    else:
        form = FoodSearch()

    return render(request, 'user_site/my_products.html', {'data': userfood_data,
                                                         'selected_data': selected_userfood_data,
                                                         'form': form})


@login_required
def product_details(request, id):
    item = get_object_or_404(ProductToUser, pk=id)
    if request.method == "POST":
        if 'update' in request.POST:
            form = NewProduct(data=request.POST)
            try:
                if form.is_valid():
                    item.product.name=form.cleaned_data['name']
                    item.product.category=form.cleaned_data['category']
                    item.product.proteins=form.cleaned_data['proteins']
                    item.product.carbohydrates=form.cleaned_data['carbohydrates']
                    item.product.sugars=form.cleaned_data['sugars']
                    item.product.fats=form.cleaned_data['fats']
                    item.product.calories=round(form.cleaned_data['proteins'] * 4 + form.cleaned_data['carbohydrates'] * 4 + form.cleaned_data['fats'] * 9)
                    item.product.save()
            except IntegrityError as e:
                if str(e).startswith("CHECK"):
                    msg = str(e)[25:]
                elif str(e).startswith("UNIQUE"):
                    msg = "Product with this name already exists. Choose another name."
                print(msg)
                return render(request, "user_site/product_details.html", {"item": item,
                                                                          "form": form,
                                                                          "msg": msg})
        elif 'delete' in request.POST:
            item.product.delete()
        return redirect('my_products')
    else:
        data = {'name': item.product.name,
                'category': item.product.category,
                'proteins': item.product.proteins,
                'carbohydrates': item.product.carbohydrates,
                'sugars': item.product.sugars,
                'fats': item.product.fats}
        form = NewProduct(data=data)
    return render(request, "user_site/product_details.html", {"item": item,
                                                              "form": form})


@login_required
def add_product(request):
    if request.method == "POST":
        form = NewProduct(data=request.POST)
        if form.is_valid():
            try:
                new_product = Products(name=form.cleaned_data['name'],
                                       category=form.cleaned_data['category'],
                                       proteins=form.cleaned_data['proteins'],
                                       carbohydrates=form.cleaned_data['carbohydrates'],
                                       sugars=form.cleaned_data['sugars'],
                                       fats=form.cleaned_data['fats'],
                                       calories=round(form.cleaned_data['proteins'] * 4 + form.cleaned_data['carbohydrates'] * 4 + form.cleaned_data['fats'] * 9))
                new_product.save()
                new_product_to_user = ProductToUser(user=request.user,
                                                    product=new_product)
                new_product_to_user.save()
            except IntegrityError as e:
                if str(e).startswith("CHECK"):
                    msg = str(e)[25:]
                elif str(e).startswith("UNIQUE"):
                    msg = "Product with this name already exists. Choose another name."
                print(msg)
                return render(request, "user_site/new_product.html", {'form': form,
                                                                      'msg': msg})
            return redirect('my_products')
    else:
        form = NewProduct()
    return render(request, "user_site/new_product.html", {'form': form})


@login_required
def week_plan(request):

    dish_data = Dish.objects.filter(user=request.user).order_by('time')

    dish_table = [["", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]]

    for dish in dish_data:
        for i in range(len(dish_table[0])):
            if dish.day == dish_table[0][i].lower():
                dish_table.append([])
                for j in range(8):
                    if j == 0:
                        dish_table[-1].append(time(hour=dish.time.hour, minute=dish.time.minute).strftime("%H:%M"))
                    else:
                        dish_table[-1].append("")
                dish_table[-1][i] = dish

    if dish_table == [["", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]]:
        dish_table = ''
    return render(request, 'user_site/week_plan.html', {'dish_table': dish_table})


@login_required
def dish_details(request, id):
    NewIngredientFormSet = create_new_ingredient_form_set(request)
    dish = get_object_or_404(Dish, pk=id)
    ingredients = Ingredients.objects.filter(dish=dish)
    if request.method == "POST":
        if 'update' in request.POST:
            dish_form = NewDish(data=request.POST)
            ing_formset = NewIngredientFormSet(data=request.POST)
            try:
                if dish_form.is_valid() and ing_formset.is_valid():
                    dish.user = request.user
                    dish.name = dish_form.cleaned_data['name']
                    dish.day = dish_form.cleaned_data['day']
                    dish.time = time(hour=dish_form.cleaned_data['time'].hour, minute=dish_form.cleaned_data['time'].minute)
                    dish.save()
                    for ing in ingredients:
                        ing.delete()
                    for item in ing_formset:
                        if item.cleaned_data == {}:
                            continue
                        else:
                            ingredient = Ingredients(dish=dish,
                                                     ingredient=item.cleaned_data['ingredient'],
                                                     mass=item.cleaned_data['mass'])
                            ingredient.save()
                else:
                    e = Error("You cannot pass only one argument to ingredient form! Only any or both are possible.")
                    msg = str(e)
                    data = {'name': dish.name,
                            'day': dish.day,
                            'time': time(hour=dish.time.hour, minute=dish.time.minute).strftime("%H:%M")}
                    dish_form = NewDish(data=data)
                    ing_formset = NewIngredientFormSet(queryset=Ingredients.objects.filter(dish=dish))
                    return render(request, "user_site/dish_details.html", {"dish": dish,
                                                                           "form": dish_form,
                                                                           "formset": ing_formset,
                                                                           "msg": msg})
            except IntegrityError as e:
                if str(e).startswith("CHECK"):
                    msg = str(e)[25:]
                elif str(e).startswith("UNIQUE"):
                    msg = "Dish planned on this day with this name or in this hour already exists. Change day, name or hour of the dish."
                data = {'name': dish.name,
                        'day': dish.day,
                        'time': time(hour=dish.time.hour, minute=dish.time.minute).strftime("%H:%M")}
                dish_form = NewDish(data=data)
                ing_formset = NewIngredientFormSet(queryset=Ingredients.objects.filter(dish=dish))
                return render(request, "user_site/dish_details.html", {"dish": dish,
                                                                       "form": dish_form,
                                                                       "formset": ing_formset,
                                                                       "msg": msg})
        elif 'delete' in request.POST:
            dish.delete()
        return redirect('week_plan')
    else:
        data = {'name': dish.name,
                'day': dish.day,
                'time': time(hour=dish.time.hour, minute=dish.time.minute).strftime("%H:%M")}
        dish_form = NewDish(data=data)
        ing_formset = NewIngredientFormSet(queryset=Ingredients.objects.filter(dish=dish))
    return render(request, "user_site/dish_details.html", {"dish": dish,
                                                           "form": dish_form,
                                                           "formset": ing_formset})


@login_required
def add_dish(request):
    NewIngredientFormSet = create_new_ingredient_form_set(request)
    if request.method == "POST":
        form = NewDish(data=request.POST)
        formset = NewIngredientFormSet(data=request.POST)
        try:
            if form.is_valid() and formset.is_valid():
                dish = Dish(user=request.user,
                            name=form.cleaned_data['name'],
                            day=form.cleaned_data['day'],
                            time=time(hour=form.cleaned_data['time'].hour, minute=form.cleaned_data['time'].minute))
                dish.save()
                for item in formset:
                    if item.cleaned_data == {}:
                        continue
                    else:
                        ingredient = Ingredients(dish=dish,
                                                 ingredient=item.cleaned_data['ingredient'],
                                                 mass=item.cleaned_data['mass'])
                        ingredient.save()
            else:
                e = Error("You cannot pass only one argument to ingredient form! Only any or both are possible.")
                msg = str(e)
                form = NewDish()
                ingredient_formset = NewIngredientFormSet(queryset=Ingredients.objects.none())
                return render(request, "user_site/new_dish.html", {"form": form,
                                                                   "formset": ingredient_formset,
                                                                   "msg": msg})
        except IntegrityError as e:
            if str(e).startswith("CHECK"):
                msg = str(e)[25:]
            elif str(e).startswith("UNIQUE"):
                msg = "Dish planned on this day with this name or in this hour already exists. Change day, name or hour of the dish."
            form = NewDish()
            ingredient_formset = NewIngredientFormSet(queryset=Ingredients.objects.none())
            return render(request, "user_site/new_dish.html", {"form": form,
                                                               "formset": ingredient_formset,
                                                               "msg": msg})
        return redirect('week_plan')
    else:
        form = NewDish()
        ingredient_formset = NewIngredientFormSet(queryset=Ingredients.objects.none())
    return render(request, "user_site/new_dish.html", {'form': form,
                                                       "formset": ingredient_formset})
