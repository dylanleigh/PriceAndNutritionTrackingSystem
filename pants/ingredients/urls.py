from django.conf.urls import url

from . import views

urlpatterns = [
   # /ingredients/
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

   # /ingredients/tag/<tag>/
   url(
      r'^tag/([0-9A-Za-z_-]+)/$',
      views.IngredientListByTagView.as_view(),
      name='ingredient-list-by-tag',
   ),

   # /ingredients/<slug>/    #NOTE: Can't be /all/, /tag/ or /csvexport/
   url(
      r'^(?P<slug>[0-9A-Za-z_-]+)/$',
      views.IngredientDetailView.as_view(),
      name='ingredient-detail',
   ),
]
