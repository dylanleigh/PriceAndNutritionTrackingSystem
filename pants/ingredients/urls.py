from django.urls import re_path
from django_filters.views import FilterView

from . import views
from .filters import IngredientFilter

urlpatterns = [
   # /ingredients/   # TODO: Make a landing page?
   re_path(r'^$', views.IngredientListView.as_view(), name='ingredient-list'),

   # /ingredients/all/
   re_path(
      r'^all/$',
      views.IngredientListAllView.as_view(),
      name='ingredient-list-all',
   ),

   # /ingredients/csvexport/
   re_path(
      r'^csvexport/$',
      views.IngredientCSVExportView,
      name='ingredient-csv-export',
   ),

   # Django-filter list
   # /ingredients/filter/<args>/
   re_path(
      r'^filter/$',
      FilterView.as_view(filterset_class=IngredientFilter),
      name='ingredient-filter',
   ),

   re_path(
      r'^tag/([0-9A-Za-z_-]+)/$',
      views.IngredientListByTagView.as_view(),
      name='ingredient-list-by-tag',
   ),

   # /ingredients/detail/<slug>/
   re_path(
      r'^detail/(?P<slug>[0-9A-Za-z_-]+)/$',
      views.IngredientDetailView.as_view(),
      name='ingredient-detail',
   ),
]
