from django.urls import re_path

from . import views

urlpatterns = [
   # /recipes/
   re_path(r'^$', views.RecipeListView.as_view(), name='recipe-list'),

   # /recipes/all/
   re_path(
      r'^all/$',
      views.RecipeListAllView.as_view(),
      name='recipe-list-all',
   ),

   # /recipe/csvexport/
   re_path(
      r'^csvexport/$',
      views.RecipeCSVExportView,
      name='recipe-csv-export',
   ),

   # /recipes/tag/<tag>/
   re_path(
      r'^tag/([0-9A-Za-z_-]+)/$',
      views.RecipeListByTagView.as_view(),
      name='recipe-list-by-tag',
   ),

   # /recipes/<slug>/
   re_path(
      r'^(?P<slug>[-\w]+)/$',
      views.RecipeDetailView.as_view(),
      name='recipe-detail'
   ),
]

