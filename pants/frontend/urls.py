from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.ingredient_manager, name='ingredient_manager'),
    url(r'^recipe$', views.recipe_manager, name='recipe_manager')
]