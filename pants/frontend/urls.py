from django.urls import re_path
from . import views

urlpatterns = [
    re_path(r'^$', views.ingredient_manager, name='ingredient_manager'),
    re_path(r'^recipe$', views.recipe_manager, name='recipe_manager')
]
