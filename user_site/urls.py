from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

urlpatterns = [
    path("login/", LoginView.as_view(template_name="login_form.html"), name="player_login"),
    path("logout/", LogoutView.as_view(), name="player_logout"),
    path("food_table/", views.food_table, name='food_table'),
    path("my_products/", views.my_products, name='my_products'),
    path("product_details/<int:id>/", views.product_details, name='product_details'),
    path("new_product/", views.add_product, name='new_product'),
    path("week_plan/", views.week_plan, name='week_plan'),
    path("dish_details/<int:id>/", views.dish_details, name='dish_details'),
    path("new_dish/", views.add_dish, name='new_dish')
]
