from django.conf.urls import url
from django_filters.views import FilterView

from . import views
from .filters import IngredientFilter

urlpatterns = [
   # /ingredients/   # TODO: Make a landing page?
   url(r'^$', views.IngredientListView.as_view(), name='ingredient-list'),

   # /ingredients/all/
   url(
      r'^all/$',
      views.IngredientListAllView.as_view(),
      name='ingredient-list-all',
   ),

   # /ingredients/csvexport/
   url(
      r'^csvexport/$',
      views.IngredientCSVExportView,
      name='ingredient-csv-export',
   ),

   # Django-filter list
   # /ingredients/list/<args>/
   url(
      r'^list/$',
      FilterView.as_view(filterset_class=IngredientFilter),
      name='ingredient-list',
   ),

   # TODO deprecated by above filter /ingredients/tag/<tag>/
   url(
      r'^tag/([0-9A-Za-z_-]+)/$',
      views.IngredientListByTagView.as_view(),
      name='ingredient-list-by-tag',
   ),

   # /ingredients/detail/<slug>/
   url(
      r'^detail/(?P<slug>[0-9A-Za-z_-]+)/$',
      views.IngredientDetailView.as_view(),
      name='ingredient-detail',
   ),
]
